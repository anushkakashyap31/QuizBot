import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FaCheckCircle, FaRedo } from 'react-icons/fa';
import { useQuizStore } from '../../store/quizStore';
import QuestionCard from './QuestionCard';
import ResultCard from './ResultCard';
import toast from 'react-hot-toast';
import { quizAPI } from '../../services/api';

const QuizInterface = ({ onRetake }) => {
  const { currentQuiz, answers, setAnswer, setQuizResult, quizResult, setLoading } = useQuizStore();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSelectAnswer = (questionId, answer) => {
    setAnswer(questionId, answer);
  };

  const handleSubmit = async () => {
    // Check if all questions are answered
    const unansweredQuestions = currentQuiz.questions.filter(q => !answers[q.id]);
    
    if (unansweredQuestions.length > 0) {
      toast.error(`Please answer all questions (${unansweredQuestions.length} remaining)`);
      return;
    }

    setIsSubmitting(true);
    setLoading(true);

    try {
      const formattedAnswers = Object.entries(answers).map(([question_id, selected_answer]) => ({
        question_id,
        selected_answer,
      }));

      const result = await quizAPI.evaluateQuiz(currentQuiz, formattedAnswers);
      setQuizResult(result);
      toast.success('Quiz submitted successfully!');
    } catch (error) {
      console.error('Error submitting quiz:', error);
      toast.error('Failed to submit quiz. Please try again.');
    } finally {
      setIsSubmitting(false);
      setLoading(false);
    }
  };

  if (!currentQuiz) {
    return null;
  }

  return (
    <div className="max-w-4xl mx-auto">
      <AnimatePresence mode="wait">
        {!quizResult ? (
          <motion.div
            key="quiz"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="space-y-6"
          >
            {/* Header */}
            <div className="card bg-gradient-to-r from-primary-500 to-secondary-500 text-white">
              <h2 className="text-2xl font-bold mb-2">Non-Profit Knowledge Assessment</h2>
              <p className="text-white/90">
                Answer all questions to test your understanding of donor relations and non-profit management
              </p>
              <div className="mt-4 flex items-center space-x-4">
                <span className="px-3 py-1 bg-white/20 rounded-full text-sm">
                  {Object.keys(answers).length} / {currentQuiz.questions.length} Answered
                </span>
              </div>
            </div>

            {/* Questions */}
            {currentQuiz.questions.map((question, index) => (
              <QuestionCard
                key={question.id}
                question={question}
                index={index}
                selectedAnswer={answers[question.id]}
                onSelectAnswer={handleSelectAnswer}
                showResult={false}
              />
            ))}

            {/* Submit Button */}
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleSubmit}
              disabled={isSubmitting}
              className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2 text-lg py-4"
            >
              {isSubmitting ? (
                <>
                  <div className="loading-spinner w-5 h-5 border-2" />
                  <span>Submitting...</span>
                </>
              ) : (
                <>
                  <FaCheckCircle />
                  <span>Submit Quiz</span>
                </>
              )}
            </motion.button>
          </motion.div>
        ) : (
          <motion.div
            key="result"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="space-y-6"
          >
            {/* Result Summary */}
            <ResultCard result={quizResult} onRetake={onRetake} />

            {/* Questions Review */}
            <div className="card">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Question Review</h3>
              <div className="space-y-6">
                {currentQuiz.questions.map((question, index) => (
                  <QuestionCard
                    key={question.id}
                    question={question}
                    index={index}
                    selectedAnswer={answers[question.id]}
                    onSelectAnswer={() => {}}
                    showResult={true}
                  />
                ))}
              </div>
            </div>

            {/* Retake Button */}
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={onRetake}
              className="w-full btn-secondary flex items-center justify-center space-x-2 text-lg py-4"
            >
              <FaRedo />
              <span>Take Another Quiz</span>
            </motion.button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default QuizInterface;