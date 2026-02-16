import React from 'react';
import { motion } from 'framer-motion';
import { FaCheckCircle, FaTimesCircle } from 'react-icons/fa';

const QuestionCard = ({ question, index, selectedAnswer, onSelectAnswer, showResult }) => {
  const isCorrect = selectedAnswer === question.correct_answer;

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.1 }}
      className="card"
    >
      {/* Question Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="flex items-center space-x-3 mb-3">
            <span className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm font-semibold">
              Question {index + 1}
            </span>
            <span className={`px-3 py-1 rounded-full text-xs font-medium ${
              question.difficulty === 'easy' ? 'bg-green-100 text-green-700' :
              question.difficulty === 'medium' ? 'bg-yellow-100 text-yellow-700' :
              'bg-red-100 text-red-700'
            }`}>
              {question.difficulty}
            </span>
          </div>
          <h3 className="text-lg font-semibold text-gray-900 leading-relaxed">
            {question.question_text}
          </h3>
        </div>
        
        {showResult && (
          <div className="ml-4">
            {isCorrect ? (
              <FaCheckCircle className="text-green-500 text-3xl" />
            ) : (
              <FaTimesCircle className="text-red-500 text-3xl" />
            )}
          </div>
        )}
      </div>

      {/* Options */}
      <div className="space-y-3">
        {question.options.map((option, idx) => {
          const optionLetter = option.charAt(0);
          const isSelected = selectedAnswer === optionLetter;
          const isCorrectOption = optionLetter === question.correct_answer;
          
          let optionClass = 'border-2 border-gray-200 hover:border-primary-300 bg-white';
          
          if (showResult) {
            if (isCorrectOption) {
              optionClass = 'border-2 border-green-500 bg-green-50';
            } else if (isSelected && !isCorrect) {
              optionClass = 'border-2 border-red-500 bg-red-50';
            } else {
              optionClass = 'border-2 border-gray-200 bg-gray-50';
            }
          } else if (isSelected) {
            optionClass = 'border-2 border-primary-500 bg-primary-50';
          }

          return (
            <motion.button
              key={idx}
              whileHover={!showResult ? { scale: 1.01 } : {}}
              whileTap={!showResult ? { scale: 0.99 } : {}}
              onClick={() => !showResult && onSelectAnswer(question.id, optionLetter)}
              disabled={showResult}
              className={`w-full p-4 rounded-xl text-left transition-all ${optionClass} ${
                showResult ? 'cursor-not-allowed' : 'cursor-pointer'
              }`}
            >
              <div className="flex items-center space-x-3">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold ${
                  showResult && isCorrectOption ? 'bg-green-500 text-white' :
                  showResult && isSelected && !isCorrect ? 'bg-red-500 text-white' :
                  isSelected ? 'bg-primary-500 text-white' :
                  'bg-gray-200 text-gray-700'
                }`}>
                  {optionLetter}
                </div>
                <span className="flex-1 text-gray-800 font-medium">
                  {option.substring(3)}
                </span>
              </div>
            </motion.button>
          );
        })}
      </div>

      {/* Explanation (shown after submission) */}
      {showResult && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          className="mt-6 p-4 bg-blue-50 border-l-4 border-blue-500 rounded-r-xl"
        >
          <h4 className="font-semibold text-blue-900 mb-2">Explanation:</h4>
          <p className="text-blue-800 leading-relaxed">{question.explanation}</p>
        </motion.div>
      )}
    </motion.div>
  );
};

export default QuestionCard;