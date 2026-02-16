import { create } from 'zustand';

export const useQuizStore = create((set) => ({
  currentQuiz: null,
  answers: {},
  quizResult: null,
  isLoading: false,
  
  setCurrentQuiz: (quiz) => set({ currentQuiz: quiz, answers: {}, quizResult: null }),
  
  setAnswer: (questionId, answer) => 
    set((state) => ({
      answers: { ...state.answers, [questionId]: answer }
    })),
  
  setQuizResult: (result) => set({ quizResult: result }),
  
  setLoading: (isLoading) => set({ isLoading }),
  
  resetQuiz: () => set({ currentQuiz: null, answers: {}, quizResult: null }),
}));