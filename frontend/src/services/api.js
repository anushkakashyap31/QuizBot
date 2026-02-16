import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
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

// Quiz API
export const quizAPI = {
  generateQuiz: async (donorEmail, numQuestions = 5) => {
    const response = await api.post('/api/quiz/generate', {
      donor_email: donorEmail,
      num_questions: numQuestions,
    });
    return response.data;
  },
  
  evaluateQuiz: async (quiz, answers) => {
    const response = await api.post('/api/quiz/evaluate', quiz, {
      params: { submission: { quiz_id: quiz.quiz_id, answers } }
    });
    return response.data;
  },
};

// Analytics API
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