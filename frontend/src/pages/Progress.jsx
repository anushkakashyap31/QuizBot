import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { FaChartLine, FaTrophy, FaFire, FaAward } from 'react-icons/fa';
import { analyticsAPI } from '../services/api';
import ProgressOverview from '../components/Dashboard/ProgressOverview';
import Loader from '../components/Common/Loader';
import toast from 'react-hot-toast';

const Progress = () => {
  const [analytics, setAnalytics] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchProgress();
  }, []);

  const fetchProgress = async () => {
    try {
      setIsLoading(true);
      const data = await analyticsAPI.getProgress();
      setAnalytics(data);
    } catch (error) {
      console.error('Error fetching progress:', error);
      toast.error('Failed to load progress data');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <Loader message="Loading progress..." />;
  }

  const achievements = [
    {
      icon: FaTrophy,
      title: 'First Quiz',
      description: 'Completed your first quiz',
      unlocked: analytics?.total_quizzes >= 1,
      color: 'bg-yellow-100 text-yellow-600',
    },
    {
      icon: FaFire,
      title: 'Hot Streak',
      description: 'Completed 5 quizzes',
      unlocked: analytics?.total_quizzes >= 5,
      color: 'bg-orange-100 text-orange-600',
    },
    {
      icon: FaAward,
      title: 'Quiz Master',
      description: 'Completed 10 quizzes',
      unlocked: analytics?.total_quizzes >= 10,
      color: 'bg-purple-100 text-purple-600',
    },
    {
      icon: FaChartLine,
      title: 'Perfectionist',
      description: 'Achieved 100% score',
      unlocked: analytics?.improvement_trend?.some(t => t.score === 100),
      color: 'bg-green-100 text-green-600',
    },
  ];

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-12"
        >
          <div className="flex items-center space-x-4 mb-4">
            <div className="p-4 bg-primary-100 rounded-xl">
              <FaChartLine className="text-primary-600 text-3xl" />
            </div>
            <div>
              <h1 className="text-4xl font-bold text-gray-900">My Progress</h1>
              <p className="text-xl text-gray-600">Track your learning journey and achievements</p>
            </div>
          </div>
        </motion.div>

        {/* Progress Overview */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-12"
        >
          <ProgressOverview analytics={analytics} />
        </motion.div>

        {/* Achievements */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Achievements</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {achievements.map((achievement, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.3 + index * 0.1 }}
                className={`card ${achievement.unlocked ? '' : 'opacity-50 grayscale'}`}
              >
                <div className={`w-16 h-16 rounded-xl flex items-center justify-center mb-4 ${achievement.color}`}>
                  <achievement.icon className="text-3xl" />
                </div>
                <h3 className="text-lg font-bold text-gray-900 mb-2">{achievement.title}</h3>
                <p className="text-sm text-gray-600 mb-3">{achievement.description}</p>
                {achievement.unlocked ? (
                  <span className="inline-block px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-semibold">
                    Unlocked ✓
                  </span>
                ) : (
                  <span className="inline-block px-3 py-1 bg-gray-100 text-gray-500 rounded-full text-xs font-semibold">
                    Locked
                  </span>
                )}
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Learning Tips */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mt-12"
        >
          <div className="card bg-gradient-to-r from-primary-50 to-secondary-50">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">💡 Learning Tips</h2>
            <ul className="space-y-3 text-gray-700">
              <li className="flex items-start">
                <span className="font-bold text-primary-600 mr-2">•</span>
                <span>Take quizzes regularly to reinforce your knowledge and track improvement</span>
              </li>
              <li className="flex items-start">
                <span className="font-bold text-primary-600 mr-2">•</span>
                <span>Review explanations carefully to understand concepts deeply</span>
              </li>
              <li className="flex items-start">
                <span className="font-bold text-primary-600 mr-2">•</span>
                <span>Focus on topics where your accuracy is below 70%</span>
              </li>
              <li className="flex items-start">
                <span className="font-bold text-primary-600 mr-2">•</span>
                <span>Set a goal to complete at least one quiz per week</span>
              </li>
            </ul>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Progress;