import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FaEnvelope, FaPaperPlane } from 'react-icons/fa';
import toast from 'react-hot-toast';
import { quizAPI } from '../../services/api';
import { useQuizStore } from '../../store/quizStore';

const EmailInput = ({ onQuizGenerated }) => {
  const [emailContent, setEmailContent] = useState('');
  const [numQuestions, setNumQuestions] = useState(5);
  const { setCurrentQuiz, setLoading } = useQuizStore();
  const [isGenerating, setIsGenerating] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!emailContent.trim()) {
      toast.error('Please enter donor email content');
      return;
    }

    setIsGenerating(true);
    setLoading(true);

    try {
      const quiz = await quizAPI.generateQuiz(emailContent, numQuestions);
      setCurrentQuiz(quiz);
      toast.success('Quiz generated successfully! 🎉');
      onQuizGenerated?.();
    } catch (error) {
      console.error('Error generating quiz:', error);
      toast.error('Failed to generate quiz. Please try again.');
    } finally {
      setIsGenerating(false);
      setLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="card max-w-4xl mx-auto"
    >
      <div className="mb-6">
        <div className="flex items-center space-x-3 mb-4">
          <div className="p-3 bg-primary-100 rounded-xl">
            <FaEnvelope className="text-primary-600 text-2xl" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Generate Quiz</h2>
            <p className="text-gray-600">Paste donor email content to create a customized assessment</p>
          </div>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Email Content */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Donor Email Content
          </label>
          <textarea
            value={emailContent}
            onChange={(e) => setEmailContent(e.target.value)}
            placeholder="Paste the donor email content here..."
            rows={12}
            className="input-field resize-none font-mono text-sm"
            required
          />
          <p className="mt-2 text-sm text-gray-500">
            {emailContent.length} characters
          </p>
        </div>

        {/* Number of Questions */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Number of Questions
          </label>
          <select
            value={numQuestions}
            onChange={(e) => setNumQuestions(Number(e.target.value))}
            className="input-field"
          >
            <option value={3}>3 Questions</option>
            <option value={5}>5 Questions (Recommended)</option>
            <option value={7}>7 Questions</option>
            <option value={10}>10 Questions</option>
          </select>
        </div>

        {/* Submit Button */}
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          type="submit"
          disabled={isGenerating}
          className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
        >
          {isGenerating ? (
            <>
              <div className="loading-spinner w-5 h-5 border-2" />
              <span>Generating Quiz...</span>
            </>
          ) : (
            <>
              <FaPaperPlane />
              <span>Generate Quiz</span>
            </>
          )}
        </motion.button>
      </form>
    </motion.div>
  );
};

export default EmailInput;