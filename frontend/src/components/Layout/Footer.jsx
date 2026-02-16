import React from 'react';
import { FaGithub, FaLinkedin, FaTwitter, FaHeart } from 'react-icons/fa';

const Footer = () => {
  return (
    <footer className="bg-white border-t border-gray-200 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-bold text-gray-900 mb-4">About QuizBot</h3>
            <p className="text-gray-600 leading-relaxed">
              QuizBot is an AI-powered educational assessment platform designed for the non-profit sector. 
              Generate intelligent quizzes from donor emails and track your learning progress.
            </p>
          </div>

          <div>
            <h3 className="text-lg font-bold text-gray-900 mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <a href="#features" className="text-gray-600 hover:text-primary-600">Features</a>
              </li>
              <li>
                <a href="#how-it-works" className="text-gray-600 hover:text-primary-600">How It Works</a>
              </li>
              <li>
                <a href="#about" className="text-gray-600 hover:text-primary-600">About</a>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="text-lg font-bold text-gray-900 mb-4">Connect</h3>
            <div className="flex space-x-4">
              <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center hover:bg-primary-100 transition-colors">
                <FaGithub className="text-gray-700" />
              </a>
              <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer" className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center hover:bg-primary-100 transition-colors">
                <FaLinkedin className="text-gray-700" />
              </a>
              <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center hover:bg-primary-100 transition-colors">
                <FaTwitter className="text-gray-700" />
              </a>
            </div>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-gray-200 text-center">
          <p className="text-gray-600 flex items-center justify-center space-x-2">
            <span>Made with</span>
            <FaHeart className="text-red-500" />
            <span>by QuizBot Team © 2025</span>
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;