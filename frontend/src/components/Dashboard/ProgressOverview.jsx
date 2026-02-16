import React from 'react';
import { motion } from 'framer-motion';
import { FaTrophy, FaChartLine, FaCheckCircle, FaBullseye } from 'react-icons/fa';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const ProgressOverview = ({ analytics }) => {
  if (!analytics) return null;

  const stats = [
    {
      icon: FaTrophy,
      label: 'Total Quizzes',
      value: analytics.total_quizzes,
      color: 'bg-primary-100 text-primary-600',
    },
    {
      icon: FaChartLine,
      label: 'Average Score',
      value: `${analytics.average_score?.toFixed(1)}%`,
      color: 'bg-green-100 text-green-600',
    },
    {
      icon: FaCheckCircle,
      label: 'Questions Answered',
      value: analytics.total_questions_answered,
      color: 'bg-blue-100 text-blue-600',
    },
    {
      icon: FaBullseye,
      label: 'Accuracy Rate',
      value: `${analytics.accuracy_rate?.toFixed(1)}%`,
      color: 'bg-purple-100 text-purple-600',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="card"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">{stat.label}</p>
                <p className="text-3xl font-bold text-gray-900">{stat.value}</p>
              </div>
              <div className={`p-3 rounded-xl ${stat.color}`}>
                <stat.icon className="text-2xl" />
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Improvement Trend Chart */}
      {analytics.improvement_trend?.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="card"
        >
          <h3 className="text-xl font-bold text-gray-900 mb-6">Performance Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={analytics.improvement_trend}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis 
                dataKey="quiz_number" 
                stroke="#6b7280"
                label={{ value: 'Quiz Number', position: 'insideBottom', offset: -5 }}
              />
              <YAxis 
                stroke="#6b7280"
                label={{ value: 'Score (%)', angle: -90, position: 'insideLeft' }}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'white', 
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px'
                }}
              />
              <Line 
                type="monotone" 
                dataKey="score" 
                stroke="#3b82f6" 
                strokeWidth={3}
                dot={{ fill: '#3b82f6', r: 5 }}
                activeDot={{ r: 7 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </motion.div>
      )}
    </div>
  );
};

export default ProgressOverview;