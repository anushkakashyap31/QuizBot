import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - Get fresh token every time
api.interceptors.request.use(
  async (config) => {
    try {
      // Import auth dynamically to avoid circular dependencies
      const { auth } = await import('./firebase');
      const user = auth.currentUser;
      
      if (user) {
        // Force token refresh to ensure it's valid
        const token = await user.getIdToken(true);
        config.headers.Authorization = `Bearer ${token}`;
        localStorage.setItem('authToken', token);
      } else {
        // Fallback to stored token
        const token = localStorage.getItem('authToken');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
      }
    } catch (error) {
      console.error('Token error:', error);
      // Continue without token, let backend reject if needed
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: async (idToken) => {
    const response = await api.post('/api/auth/login', { id_token: idToken });
    return response.data;
  },
  getCurrentUser: async () => {
    const response = await api.get('/api/auth/me');
    return response.data;
  },
};

export const quizAPI = {
  generateQuiz: async (donorEmail, numQuestions = 5) => {
    const response = await api.post('/api/quiz/generate', {
      donor_email: donorEmail,
      num_questions: numQuestions,
    });
    return response.data;
  },
  evaluateQuiz: async (quiz, answers) => {
    const response = await api.post('/api/quiz/evaluate', {
      quiz: quiz,
      answers: answers,
    });
    return response.data;
  },
};

export const analyticsAPI = {
  getHistory: async () => {
    const response = await api.get('/api/analytics/history');
    return response.data;
  },
  getProgress: async () => {
    const response = await api.get('/api/analytics/progress');
    return response.data;
  },
  getStats: async () => {
    const response = await api.get('/api/analytics/stats');
    return response.data;
  },
};

export default api;