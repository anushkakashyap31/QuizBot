import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { FaRocket, FaBrain, FaChartLine, FaUsers, FaCheckCircle, FaLightbulb } from 'react-icons/fa';

const Home = () => {
  const features = [
    {
      icon: FaBrain,
      title: 'AI-Powered Quizzes',
      description: 'Generate intelligent quizzes from donor emails using advanced AI technology',
    },
    {
      icon: FaChartLine,
      title: 'Track Progress',
      description: 'Monitor your learning journey with detailed analytics and insights',
    },
    {
      icon: FaLightbulb,
      title: 'Deep Explanations',
      description: 'Learn from detailed explanations for every question',
    },
    {
      icon: FaUsers,
      title: 'Non-Profit Focus',
      description: 'Specialized content for donor relations and non-profit management',
    },
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left Content */}
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
            >
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.2 }}
                className="inline-block px-4 py-2 bg-primary-100 rounded-full mb-6"
              >
                <span className="text-primary-700 font-semibold">🎉 Welcome to QuizBot</span>
              </motion.div>
              
              <h1 className="text-5xl lg:text-6xl font-bold text-gray-900 mb-6 leading-tight">
                Master{' '}
                <span className="text-gradient">Non-Profit</span>
                {' '}Knowledge with AI
              </h1>
              
              <p className="text-xl text-gray-600 mb-8 leading-relaxed">
                Transform donor emails into engaging assessments. Track your progress, 
                receive detailed feedback, and become an expert in non-profit management.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4">
                <Link to="/register" className="btn-primary text-center">
                  Get Started Free
                </Link>
                <Link to="/login" className="btn-secondary text-center">
                  Sign In
                </Link>
              </div>
            </motion.div>

            {/* Right Content - Animated Illustration */}
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="relative"
            >
              <div className="glass-card p-8">
                <motion.div
                  animate={{ y: [0, -10, 0] }}
                  transition={{ duration: 2, repeat: Infinity }}
                  className="bg-gradient-to-br from-primary-500 to-secondary-500 rounded-2xl p-8 text-white"
                >
                  <FaRocket className="text-6xl mb-4" />
                  <h3 className="text-2xl font-bold mb-2">Start Learning Today</h3>
                  <p className="text-white/90">Generate your first AI-powered quiz in seconds</p>
                </motion.div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 bg-white">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Everything You Need to Learn
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Powerful features designed to enhance your non-profit education
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="card hover:shadow-2xl transition-shadow"
              >
                <div className="w-14 h-14 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-xl flex items-center justify-center mb-4">
                  <feature.icon className="text-white text-2xl" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              How QuizBot Works
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Three simple steps to start your learning journey
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                step: '1',
                title: 'Input Donor Email',
                description: 'Paste donor email content into QuizBot',
              },
              {
                step: '2',
                title: 'Generate Quiz',
                description: 'AI creates customized questions based on content',
              },
              {
                step: '3',
                title: 'Learn & Improve',
                description: 'Get detailed feedback and track your progress',
              },
            ].map((step, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.2 }}
                className="text-center"
              >
                <div className="w-16 h-16 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
                  {step.step}
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">{step.title}</h3>
                <p className="text-gray-600">{step.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-gradient-to-r from-primary-600 to-secondary-600">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl font-bold text-white mb-6">
              Ready to Start Learning?
            </h2>
            <p className="text-xl text-white/90 mb-8">
              Join QuizBot today and transform your non-profit knowledge
            </p>
            <Link to="/register" className="btn-secondary bg-white hover:bg-gray-50">
              Get Started Now
            </Link>
          </motion.div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-20 px-4 bg-white">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center"
          >
            <h2 className="text-4xl font-bold text-gray-900 mb-6">About QuizBot</h2>
            <div className="prose prose-lg mx-auto text-gray-600">
              <p>
                QuizBot is an innovative AI-driven educational assessment platform specifically designed 
                for the non-profit sector. Our mission is to bridge knowledge gaps and enhance understanding 
                of donor relations, fundraising strategies, and non-profit management through intelligent, 
                contextual learning.
              </p>
              <p>
                By leveraging cutting-edge language models, QuizBot transforms donor emails into meaningful 
                assessments that test comprehension and application, not just recall. Our platform provides 
                detailed explanations, personalized feedback, and comprehensive analytics to support your 
                continuous learning journey.
              </p>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default Home;