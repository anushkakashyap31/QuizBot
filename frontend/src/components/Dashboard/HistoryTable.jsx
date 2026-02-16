import React from 'react';
import { motion } from 'framer-motion';
import { FaTrophy, FaCalendar, FaCheckCircle } from 'react-icons/fa';
import { format } from 'date-fns';

const HistoryTable = ({ history }) => {
  if (!history || history.length === 0) {
    return (
      <div className="card text-center py-12">
        <p className="text-gray-500">No quiz history yet. Take your first quiz!</p>
      </div>
    );
  }

  const getGradeColor = (score) => {
    if (score >= 90) return 'text-green-600 bg-green-100';
    if (score >= 80) return 'text-blue-600 bg-blue-100';
    if (score >= 70) return 'text-yellow-600 bg-yellow-100';
    if (score >= 60) return 'text-orange-600 bg-orange-100';
    return 'text-red-600 bg-red-100';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="card overflow-hidden"
    >
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-bold text-gray-900">Quiz History</h3>
        <span className="text-sm text-gray-500">{history.length} total quizzes</span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b-2 border-gray-200">
              <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Date</th>
              <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Score</th>
              <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Questions</th>
              <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Correct</th>
              <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Grade</th>
            </tr>
          </thead>
          <tbody>
            {history.map((quiz, index) => (
              <motion.tr
                key={quiz.quiz_id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                className="border-b border-gray-100 hover:bg-gray-50 transition-colors"
              >
                <td className="py-4 px-4">
                  <div className="flex items-center space-x-2">
                    <FaCalendar className="text-gray-400" />
                    <span className="text-sm text-gray-700">
                      {format(new Date(quiz.completed_at), 'MMM dd, yyyy')}
                    </span>
                  </div>
                </td>
                <td className="py-4 px-4">
                  <div className="flex items-center space-x-2">
                    <FaTrophy className="text-yellow-500" />
                    <span className="font-semibold text-gray-900">
                      {quiz.score.toFixed(1)}%
                    </span>
                  </div>
                </td>
                <td className="py-4 px-4">
                  <span className="text-gray-700">{quiz.total_questions}</span>
                </td>
                <td className="py-4 px-4">
                  <div className="flex items-center space-x-2">
                    <FaCheckCircle className="text-green-500" />
                    <span className="text-gray-700">
                      {quiz.correct_answers}/{quiz.total_questions}
                    </span>
                  </div>
                </td>
                <td className="py-4 px-4">
                  <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getGradeColor(quiz.score)}`}>
                    {quiz.score >= 90 ? 'A' :
                     quiz.score >= 80 ? 'B' :
                     quiz.score >= 70 ? 'C' :
                     quiz.score >= 60 ? 'D' : 'F'}
                  </span>
                </td>
              </motion.tr>
            ))}
          </tbody>
        </table>
      </div>
    </motion.div>
  );
};

export default HistoryTable;