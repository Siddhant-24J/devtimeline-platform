'use client';

import React from 'react';
import { Github, Sparkles, ShieldCheck, CheckCircle2, ArrowRight } from 'lucide-react';
import { API_BASE } from '@/lib/api';

export default function LoginPage() {
  const handleGitHubAuth = () => {
    window.location.href = `${API_BASE}/api/auth/github/login`;
  };

  return (
    <div id="login-container" className="min-h-[80vh] flex items-center justify-center py-12">
      <div className="glass-card p-8 md:p-12 rounded-3xl max-w-md w-full text-center space-y-8 border border-indigo-500/20 shadow-2xl">
        <div className="space-y-3">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-indigo-600 via-purple-600 to-pink-500 mx-auto flex items-center justify-center shadow-lg">
            <Github className="w-8 h-8 text-white" />
          </div>

          <h1 className="text-3xl font-extrabold text-white">Sign In to DevTimeline</h1>
          <p className="text-xs text-gray-400 leading-relaxed">
            Authorize DevTimeline GitHub App to connect your repositories, generate project roadmaps, and push automated development commits.
          </p>
        </div>

        {/* Benefits list */}
        <div className="space-y-2 text-left bg-surface/50 p-4 rounded-2xl border border-surface-border text-xs text-gray-300">
          <div className="flex items-center space-x-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
            <span>Minimal scopes (`repo`, `user:email`) requested</span>
          </div>
          <div className="flex items-center space-x-2">
            <CheckCircle2 className="w-4 h-4 text-purple-400 flex-shrink-0" />
            <span>Isolated branch commits (`devtimeline/day-X`)</span>
          </div>
          <div className="flex items-center space-x-2">
            <CheckCircle2 className="w-4 h-4 text-indigo-400 flex-shrink-0" />
            <span>Zero password storage — Tokens encrypted</span>
          </div>
        </div>

        {/* Action Button */}
        <button
          id="github-oauth-login-btn"
          onClick={handleGitHubAuth}
          className="w-full py-3.5 px-6 rounded-xl bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:from-indigo-500 hover:to-pink-500 text-white font-bold text-sm shadow-xl hover:shadow-indigo-500/30 transition-all duration-200 flex items-center justify-center space-x-2"
        >
          <Github className="w-5 h-5" />
          <span>Continue with GitHub</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
