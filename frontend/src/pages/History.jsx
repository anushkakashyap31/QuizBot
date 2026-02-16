import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { FaHistory, FaSearch } from 'react-icons/fa';
import { analyticsAPI } from '../services/api';
import HistoryTable from '../components/Dashboard/HistoryTable';
import Loader from '../components/Common/Loader';
import toast from 'react-hot-toast';

const History = () => {
  const [history, setHistory] = useState([]);
  const [filteredHistory, setFilteredHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchHistory();
  }, []);

  useEffect(() => {
    if (searchTerm) {
      const filtered = history.filter(quiz => 
        new Date(quiz.completed_at).toLocaleDateString().includes(searchTerm) ||
        quiz.score.toString().includes(searchTerm)
      );
      setFilteredHistory(filtered);
    } else {
      setFilteredHistory(history);
    }
  }, [searchTerm, history]);

  const fetchHistory = async () => {
    try {
      setIsLoading(true);
      const data = await analyticsAPI.getHistory();
      setHistory(data);
      setFilteredHistory(data);
    } catch (error) {
      console.error('Error fetching history:', error);
      toast.error('Failed to load quiz history');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <Loader message="Loading quiz history..." />;
  }

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
              <FaHistory className="text-primary-600 text-3xl" />
            </div>
            <div>
              <h1 className="text-4xl font-bold text-gray-900">Quiz History</h1>
              <p className="text-xl text-gray-600">Review your past assessments and performance</p>
            </div>
          </div>
        </motion.div>

        {/* Search */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-8"
        >
          <div className="relative max-w-md">
            <FaSearch className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="Search by date or score..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input-field pl-12"
            />
          </div>
        </motion.div>

        {/* History Table */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <HistoryTable history={filteredHistory} />
        </motion.div>
      </div>
    </div>
  );
};

export default History;