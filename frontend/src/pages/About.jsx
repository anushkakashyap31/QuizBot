import React from 'react';
import { motion } from 'framer-motion';
import { FaRocket, FaBrain, FaUsers, FaHeart } from 'react-icons/fa';

const About = () => {
  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-bold text-gradient mb-4">About QuizBot</h1>
          <p className="text-xl text-gray-600">
            Transforming non-profit education with AI-powered assessments
          </p>
        </motion.div>

        {/* Mission Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card mb-8"
        >
          <div className="flex items-center space-x-4 mb-6">
            <div className="p-4 bg-primary-100 rounded-xl">
              <FaRocket className="text-primary-600 text-3xl" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900">Our Mission</h2>
          </div>
          <p className="text-gray-700 leading-relaxed mb-4">
            QuizBot is dedicated to enhancing educational outcomes in the non-profit sector through
            intelligent, AI-driven assessments. We believe that effective learning requires more than
            just testing knowledge—it requires deep understanding, contextual application, and
            continuous improvement.
          </p>
          <p className="text-gray-700 leading-relaxed">
            By leveraging cutting-edge language models, we transform donor communications into
            meaningful learning experiences that test comprehension, not just recall.
          </p>
        </motion.div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="card text-center"
          >
            <div className="w-16 h-16 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <FaBrain className="text-white text-2xl" />
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-2">AI-Powered</h3>
            <p className="text-gray-600 text-sm">
              Advanced AI generates contextual questions from any donor email content
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="card text-center"
          >
            <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <FaUsers className="text-white text-2xl" />
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-2">Non-Profit Focus</h3>
            <p className="text-gray-600 text-sm">
              Specialized content for donor relations and non-profit management
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="card text-center"
          >
            <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <FaHeart className="text-white text-2xl" />
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-2">Personalized Learning</h3>
            <p className="text-gray-600 text-sm">
              Detailed feedback and analytics tailored to your learning journey
            </p>
          </motion.div>
        </div>

        {/* Technology Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="card"
        >
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Technology Stack</h2>
          <div className="space-y-3 text-gray-700">
            <p>
              <strong className="text-primary-600">Frontend:</strong> React, Tailwind CSS, Framer Motion, Firebase Authentication
            </p>
            <p>
              <strong className="text-primary-600">Backend:</strong> Python, FastAPI, Google Gemini AI
            </p>
            <p>
              <strong className="text-primary-600">Database:</strong> Firebase Realtime Database, ChromaDB Vector Store
            </p>
            <p>
              <strong className="text-primary-600">AI:</strong> Google Gemini Pro for intelligent quiz generation and evaluation
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default About;