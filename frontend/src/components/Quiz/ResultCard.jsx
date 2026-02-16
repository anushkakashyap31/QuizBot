import React from 'react';
import { motion } from 'framer-motion';
import { FaTrophy, FaStar, FaChartLine, FaCheckCircle, FaTimesCircle } from 'react-icons/fa';

const ResultCard = ({ result, onRetake }) => {
  const { score, total_questions, correct_answers, summary } = result;
  
  const getGrade = () => {
    if (score >= 90) return { letter: 'A', color: 'text-green-600', bg: 'bg-green-100' };
    if (score >= 80) return { letter: 'B', color: 'text-blue-600', bg: 'bg-blue-100' };
    if (score >= 70) return { letter: 'C', color: 'text-yellow-600', bg: 'bg-yellow-100' };
    if (score >= 60) return { letter: 'D', color: 'text-orange-600', bg: 'bg-orange-100' };
    return { letter: 'F', color: 'text-red-600', bg: 'bg-red-100' };
  };

  const grade = getGrade();

  const getPerformanceMessage = () => {
    if (score >= 90) return { text: '🎉 Outstanding!', color: 'text-green-600' };
    if (score >= 80) return { text: '✨ Excellent!', color: 'text-blue-600' };
    if (score >= 70) return { text: '👍 Good Job!', color: 'text-yellow-600' };
    if (score >= 60) return { text: '💪 Keep Trying!', color: 'text-orange-600' };
    return { text: '📚 More Practice Needed', color: 'text-red-600' };
  };

  const performance = getPerformanceMessage();

  return (
    <motion.div
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      className="card bg-gradient-to-br from-primary-50 to-secondary-50 border-2 border-primary-200"
    >
      {/* Header */}
      <div className="text-center mb-8">
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', stiffness: 200, delay: 0.2 }}
          className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-full mb-4"
        >
          <FaTrophy className="text-white text-4xl" />
        </motion.div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Quiz Complete!</h2>
        <p className={`text-2xl font-bold ${performance.color}`}>{performance.text}</p>
      </div>

      {/* Score Display */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {/* Overall Score */}
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-xl p-6 text-center shadow-lg"
        >
          <div className={`w-16 h-16 mx-auto mb-3 rounded-full flex items-center justify-center ${grade.bg}`}>
            <span className={`text-3xl font-bold ${grade.color}`}>{grade.letter}</span>
          </div>
          <p className="text-4xl font-bold text-gray-900 mb-1">{score.toFixed(1)}%</p>
          <p className="text-sm text-gray-600">Overall Score</p>
        </motion.div>

        {/* Correct Answers */}
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="bg-white rounded-xl p-6 text-center shadow-lg"
        >
          <FaCheckCircle className="w-16 h-16 mx-auto mb-3 text-green-500" />
          <p className="text-4xl font-bold text-gray-900 mb-1">
            {correct_answers}/{total_questions}
          </p>
          <p className="text-sm text-gray-600">Correct Answers</p>
        </motion.div>

        {/* Incorrect Answers */}
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="bg-white rounded-xl p-6 text-center shadow-lg"
        >
          <FaTimesCircle className="w-16 h-16 mx-auto mb-3 text-red-500" />
          <p className="text-4xl font-bold text-gray-900 mb-1">
            {total_questions - correct_answers}/{total_questions}
          </p>
          <p className="text-sm text-gray-600">Incorrect Answers</p>
        </motion.div>
      </div>

      {/* Performance Summary */}
      <motion.div
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.6 }}
        className="bg-white rounded-xl p-6 shadow-lg"
      >
        <div className="flex items-center space-x-3 mb-4">
          <FaChartLine className="text-primary-600 text-2xl" />
          <h3 className="text-xl font-bold text-gray-900">Performance Summary</h3>
        </div>
        <div className="prose prose-sm max-w-none text-gray-700 leading-relaxed">
          {summary?.split('\n').map((paragraph, index) => (
            paragraph.trim() && (
              <p key={index} className="mb-3">{paragraph}</p>
            )
          ))}
        </div>
      </motion.div>

      {/* Progress Bar */}
      <motion.div
        initial={{ scaleX: 0 }}
        animate={{ scaleX: 1 }}
        transition={{ delay: 0.7, duration: 0.5 }}
        className="mt-6"
      >
        <div className="flex justify-between text-sm font-medium text-gray-700 mb-2">
          <span>Progress</span>
          <span>{score.toFixed(0)}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${score}%` }}
            transition={{ delay: 0.8, duration: 0.8 }}
            className={`h-full rounded-full ${
              score >= 80 ? 'bg-gradient-to-r from-green-500 to-green-600' :
              score >= 60 ? 'bg-gradient-to-r from-yellow-500 to-yellow-600' :
              'bg-gradient-to-r from-red-500 to-red-600'
            }`}
          />
        </div>
      </motion.div>
    </motion.div>
  );
};

export default ResultCard;