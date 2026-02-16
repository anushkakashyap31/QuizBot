import React, { useState } from 'react';
import { motion } from 'framer-motion';
import EmailInput from '../components/Quiz/EmailInput';
import QuizInterface from '../components/Quiz/QuizInterface';
import { useQuizStore } from '../store/quizStore';

const QuizPage = () => {
  const { currentQuiz, resetQuiz } = useQuizStore();
  const [showQuiz, setShowQuiz] = useState(false);

  const handleQuizGenerated = () => {
    setShowQuiz(true);
  };

  const handleRetake = () => {
    resetQuiz();
    setShowQuiz(false);
  };

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-bold text-gradient mb-4">
            {!showQuiz ? 'Create Your Quiz' : 'Quiz Assessment'}
          </h1>
          <p className="text-xl text-gray-600">
            {!showQuiz 
              ? 'Generate an AI-powered quiz from donor email content' 
              : 'Answer all questions to test your knowledge'}
          </p>
        </motion.div>

        {!showQuiz || !currentQuiz ? (
          <EmailInput onQuizGenerated={handleQuizGenerated} />
        ) : (
          <QuizInterface onRetake={handleRetake} />
        )}
      </div>
    </div>
  );
};

export default QuizPage;