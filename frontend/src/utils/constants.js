// API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// App Configuration
export const APP_NAME = 'QuizBot';
export const APP_VERSION = '1.0.0';

// Quiz Configuration
export const DEFAULT_NUM_QUESTIONS = 5;
export const MIN_QUESTIONS = 3;
export const MAX_QUESTIONS = 10;

// Difficulty Levels
export const DIFFICULTY_LEVELS = {
  EASY: 'easy',
  MEDIUM: 'medium',
  HARD: 'hard',
};

// Grade Thresholds
export const GRADE_THRESHOLDS = {
  A: 90,
  B: 80,
  C: 70,
  D: 60,
  F: 0,
};

// Performance Labels
export const PERFORMANCE_LABELS = {
  EXCELLENT: 'Excellent',
  VERY_GOOD: 'Very Good',
  GOOD: 'Good',
  FAIR: 'Fair',
  NEEDS_IMPROVEMENT: 'Needs Improvement',
};

// Toast Duration
export const TOAST_DURATION = 3000;

// Local Storage Keys
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'authToken',
  USER: 'user',
  THEME: 'theme',
};

// Routes
export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  DASHBOARD: '/dashboard',
  QUIZ: '/quiz',
  HISTORY: '/history',
  PROGRESS: '/progress',
};

// Animation Delays
export const ANIMATION_DELAYS = {
  FAST: 0.1,
  MEDIUM: 0.2,
  SLOW: 0.3,
};

export default {
  API_BASE_URL,
  APP_NAME,
  APP_VERSION,
  DEFAULT_NUM_QUESTIONS,
  MIN_QUESTIONS,
  MAX_QUESTIONS,
  DIFFICULTY_LEVELS,
  GRADE_THRESHOLDS,
  PERFORMANCE_LABELS,
  TOAST_DURATION,
  STORAGE_KEYS,
  ROUTES,
  ANIMATION_DELAYS,
};