import React from 'react';
import Link from 'next/link';
import { 
  GitBranch, 
  Sparkles, 
  ArrowRight, 
  Github, 
  FolderUp, 
  BookOpen, 
  CheckCircle2, 
  ShieldCheck, 
  Clock, 
  Terminal,
  Cpu
} from 'lucide-react';

export default function LandingPage() {
  return (
    <div id="landing-container" className="space-y-16 py-6">
      {/* Hero Header */}
      <section className="text-center space-y-6 max-w-4xl mx-auto pt-6">
        <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 text-xs font-semibold">
          <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
          <span>AI-Powered Project Development & Automation Platform</span>
        </div>

        <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight leading-tight">
          Plan Your Project. <br />
          <span className="gradient-text-primary">Build Progressively.</span> <br />
          Sync with GitHub.
        </h1>

        <p className="text-lg md:text-xl text-gray-400 max-w-2xl mx-auto leading-relaxed">
          DevTimeline analyzes your repository or project template, generates a dependency-aware roadmap, and executes daily commits to maintain genuine development momentum.
        </p>

        <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
          <Link
            href="/dashboard"
            id="hero-get-started-btn"
            className="flex items-center space-x-2 px-6 py-3.5 text-sm font-semibold rounded-xl bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:from-indigo-500 hover:to-pink-500 text-white shadow-xl hover:shadow-indigo-500/30 transition-all duration-200 group"
          >
            <span>Open Dashboard</span>
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </Link>

          <Link
            href="/library"
            id="hero-browse-library-btn"
            className="flex items-center space-x-2 px-6 py-3.5 text-sm font-semibold rounded-xl bg-surface/80 hover:bg-surface-border border border-surface-border text-gray-200 transition-all duration-200"
          >
            <BookOpen className="w-4 h-4 text-purple-400" />
            <span>Browse Project Library</span>
          </Link>
        </div>
      </section>

      {/* 3 Ingestion Sources Showcase */}
      <section className="grid md:grid-cols-3 gap-6 pt-4">
        <div className="glass-card p-6 rounded-2xl glass-card-hover space-y-4 border border-indigo-500/20">
          <div className="w-12 h-12 rounded-xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
            <Github className="w-6 h-6" />
          </div>
          <h3 className="text-xl font-bold text-white">Existing GitHub Repo</h3>
          <p className="text-sm text-gray-400 leading-relaxed">
            Connect your existing GitHub repository. DevTimeline scans your existing codebase, detects missing features, and plans a structured roadmap.
          </p>
        </div>

        <div className="glass-card p-6 rounded-2xl glass-card-hover space-y-4 border border-purple-500/20">
          <div className="w-12 h-12 rounded-xl bg-purple-600/20 border border-purple-500/30 flex items-center justify-center text-purple-400">
            <FolderUp className="w-6 h-6" />
          </div>
          <h3 className="text-xl font-bold text-white">Upload Project ZIP</h3>
          <p className="text-sm text-gray-400 leading-relaxed">
            Upload local source archives. Our project analyzer inspects technologies, creates a brand new GitHub repo, and schedules daily milestones.
          </p>
        </div>

        <div className="glass-card p-6 rounded-2xl glass-card-hover space-y-4 border border-pink-500/20">
          <div className="w-12 h-12 rounded-xl bg-pink-600/20 border border-pink-500/30 flex items-center justify-center text-pink-400">
            <BookOpen className="w-6 h-6" />
          </div>
          <h3 className="text-xl font-bold text-white">Built-in Project Library</h3>
          <p className="text-sm text-gray-400 leading-relaxed">
            Choose from fully functional beginner, intermediate, and advanced projects (Portfolio, E-Commerce, Intrusion Detection, AI Chatbot).
          </p>
        </div>
      </section>

      {/* Feature Capabilities Grid */}
      <section className="glass-card p-8 rounded-3xl space-y-8">
        <div className="text-center space-y-2 max-w-xl mx-auto">
          <h2 className="text-2xl md:text-3xl font-bold text-white">Engineering Architecture</h2>
          <p className="text-sm text-gray-400">Designed for legitimate software orchestration and GitHub commit synchronization.</p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="p-4 rounded-xl bg-surface/50 border border-surface-border space-y-2">
            <Cpu className="w-5 h-5 text-indigo-400" />
            <h4 className="font-semibold text-white text-sm">Static Analysis</h4>
            <p className="text-xs text-gray-400">Language, framework & DB dependency detector.</p>
          </div>

          <div className="p-4 rounded-xl bg-surface/50 border border-surface-border space-y-2">
            <Clock className="w-5 h-5 text-purple-400" />
            <h4 className="font-semibold text-white text-sm">Flexible Duration</h4>
            <p className="text-xs text-gray-400">Customizable 7 to 90-day development plans.</p>
          </div>

          <div className="p-4 rounded-xl bg-surface/50 border border-surface-border space-y-2">
            <Terminal className="w-5 h-5 text-pink-400" />
            <h4 className="font-semibold text-white text-sm">Validation Engine</h4>
            <p className="text-xs text-gray-400">Automated test runners and syntax check sandboxing.</p>
          </div>

          <div className="p-4 rounded-xl bg-surface/50 border border-surface-border space-y-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            <h4 className="font-semibold text-white text-sm">Isolated Sandboxing</h4>
            <p className="text-xs text-gray-400">Feature branch creation prior to GitHub merges.</p>
          </div>
        </div>
      </section>
    </div>
  );
}
