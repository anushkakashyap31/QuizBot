import { 
  signInWithEmailAndPassword, 
  createUserWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  updateProfile
} from 'firebase/auth';
import { auth } from './firebase';
import { authAPI } from './api';

export const authService = {
  // Sign up new user
  signup: async (email, password, fullName) => {
    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      
      // Update profile with full name
      await updateProfile(userCredential.user, {
        displayName: fullName
      });
      
      // Get ID token
      const idToken = await userCredential.user.getIdToken();
      
      // Login to backend
      const response = await authAPI.login(idToken);
      localStorage.setItem('authToken', response.access_token);
      
      return response;
    } catch (error) {
      throw error;
    }
  },

  // Login existing user
  login: async (email, password) => {
    try {
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      const idToken = await userCredential.user.getIdToken();
      
      // Login to backend
      const response = await authAPI.login(idToken);
      localStorage.setItem('authToken', response.access_token);
      
      return response;
    } catch (error) {
      throw error;
    }
  },

  // Logout
  logout: async () => {
    try {
      await signOut(auth);
      localStorage.removeItem('authToken');
    } catch (error) {
      throw error;
    }
  },

  // Get current user
  getCurrentUser: () => {
    return auth.currentUser;
  },

  // Auth state observer
  onAuthStateChanged: (callback) => {
    return onAuthStateChanged(auth, callback);
  },
};

export default authService;