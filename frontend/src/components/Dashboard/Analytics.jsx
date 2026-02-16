import React from 'react';
import { motion } from 'framer-motion';
import { FaChartBar, FaTrendingUp, FaAward } from 'react-icons/fa';

const Analytics = ({ data }) => {
  // This is an optional analytics component
  // Can be used for more detailed analytics visualization
  
  return (
    <div className="card">
      <h3 className="text-xl font-bold text-gray-900 mb-6">Detailed Analytics</h3>
      <p className="text-gray-600">More detailed analytics coming soon...</p>
    </div>
  );
};

export default Analytics;