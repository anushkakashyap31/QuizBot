import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { FaRocket, FaHistory, FaChartLine, FaPlus } from 'react-icons/fa';
import { analyticsAPI } from '../services/api';
import { useAuthStore } from '../store/authStore';
import ProgressOverview from '../components/Dashboard/ProgressOverview';
import HistoryTable from '../components/Dashboard/HistoryTable';
import Loader from '../components/Common/Loader';
import toast from 'react-hot-toast';

const Dashboard = () => {
  const { user } = useAuthStore();
  const [analytics, setAnalytics] = useState(null);
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setIsLoading(true);
      const [analyticsData, historyData] = await Promise.all([
        analyticsAPI.getProgress(),
        analyticsAPI.getHistory(),
      ]);
      setAnalytics(analyticsData);
      setHistory(historyData.slice(0, 5)); // Show only recent 5
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <Loader message="Loading dashboard..." />;
  }

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Welcome Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-12"
        >
          <div className="glass-card p-8 bg-gradient-to-r from-primary-500 to-secondary-500 text-white">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-4xl font-bold mb-2">
                  Welcome back, {user?.full_name || 'Learner'}! 👋
                </h1>
                <p className="text-white/90 text-lg">
                  Ready to continue your learning journey?
                </p>
              </div>
              <motion.div
                animate={{ rotate: [0, 10, -10, 0] }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                <FaRocket className="text-6xl opacity-50" />
              </motion.div>
            </div>
          </div>
        </motion.div>

        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid md:grid-cols-3 gap-6 mb-12"
        >
          <Link
            to="/quiz"
            className="card hover:shadow-2xl transition-all group"
          >
            <div className="flex items-center space-x-4">
              <div className="p-4 bg-primary-100 rounded-xl group-hover:bg-primary-200 transition-colors">
                <FaPlus className="text-primary-600 text-2xl" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-gray-900">New Quiz</h3>
                <p className="text-sm text-gray-600">Start a new assessment</p>
              </div>
            </div>
          </Link>

          <Link
            to="/history"
            className="card hover:shadow-2xl transition-all group"
          >
            <div className="flex items-center space-x-4">
              <div className="p-4 bg-blue-100 rounded-xl group-hover:bg-blue-200 transition-colors">
                <FaHistory className="text-blue-600 text-2xl" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-gray-900">Quiz History</h3>
                <p className="text-sm text-gray-600">View past quizzes</p>
              </div>
            </div>
          </Link>

          <Link
            to="/progress"
            className="card hover:shadow-2xl transition-all group"
          >
            <div className="flex items-center space-x-4">
              <div className="p-4 bg-green-100 rounded-xl group-hover:bg-green-200 transition-colors">
                <FaChartLine className="text-green-600 text-2xl" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-gray-900">My Progress</h3>
                <p className="text-sm text-gray-600">Track performance</p>
              </div>
            </div>
          </Link>
        </motion.div>

        {/* Progress Overview */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-12"
        >
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Performance Overview</h2>
          <ProgressOverview analytics={analytics} />
        </motion.div>

        {/* Recent History */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Recent Quizzes</h2>
            <Link to="/history" className="text-primary-600 hover:text-primary-700 font-semibold">
              View All →
            </Link>
          </div>
          <HistoryTable history={history} />
        </motion.div>
      </div>
    </div>
  );
};

export default Dashboard;