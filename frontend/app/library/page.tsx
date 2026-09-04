'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { 
  BookOpen, 
  Search, 
  Filter, 
  Clock, 
  Sparkles, 
  Code2, 
  CheckCircle2, 
  ArrowRight,
  Shield,
  Layers,
  Bot
} from 'lucide-react';
import { API_BASE } from '../../lib/api';

interface Template {
  id: number;
  name: string;
  slug: string;
  description: string;
  difficulty: string;
  category: string;
  tech_stack: string;
  estimated_days: number;
  features?: string;
}

export default function LibraryPage() {
  const router = useRouter();
  const [templates, setTemplates] = useState<Template[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDifficulty, setSelectedDifficulty] = useState('ALL');
  const [selectedTemplate, setSelectedTemplate] = useState<Template | null>(null);
  const [selectedDuration, setSelectedDuration] = useState<number>(30);
  const [isStarting, setIsStarting] = useState(false);

  useEffect(() => {
    fetch(`${API_BASE}/api/templates/`)
      .then(res => res.json())
      .then(data => setTemplates(data))
      .catch(() => {
        // Fallback default templates if backend compiling
        setTemplates([
          {
            id: 1,
            name: "Personal Developer Portfolio",
            slug: "personal-portfolio",
            description: "High-performance developer portfolio showcasing projects, experience timeline, responsive design, interactive micro-animations, and contact form.",
            difficulty: "BEGINNER",
            category: "Frontend",
            tech_stack: "Next.js, TypeScript, Tailwind CSS, Framer Motion",
            estimated_days: 14
          },
          {
            id: 2,
            name: "E-Commerce Commerce Platform",
            slug: "ecommerce-platform",
            description: "Full-stack digital storefront with product catalog search, inventory management, shopping cart, Stripe payment gateway, and admin dashboard.",
            difficulty: "INTERMEDIATE",
            category: "Fullstack",
            tech_stack: "Next.js, FastAPI, PostgreSQL, Stripe",
            estimated_days: 30
          },
          {
            id: 3,
            name: "Network Intrusion Detection System (IDS)",
            slug: "intrusion-detection-system",
            description: "Machine-learning driven network packet analyzer detecting suspicious traffic, malicious anomalies, signatures, and real-time alert visualization.",
            difficulty: "ADVANCED",
            category: "Security / AI",
            tech_stack: "Python, Scapy, PyTorch, FastAPI, React",
            estimated_days: 60
          },
          {
            id: 4,
            name: "AI Assistant Chatbot Platform",
            slug: "ai-chatbot-platform",
            description: "Enterprise-grade RAG AI chatbot platform with document vector search, prompt history, multi-persona engine, and customizable LLM pipelines.",
            difficulty: "ADVANCED",
            category: "AI / ML",
            tech_stack: "Next.js, FastAPI, LangChain, FAISS, Gemini",
            estimated_days: 45
          }
        ]);
      });
  }, []);

  const handleStartProject = async (template: Template) => {
    setIsStarting(true);
    try {
      const res = await fetch(`${API_BASE}/api/projects/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: template.name,
          description: template.description,
          source_type: 'BUILTIN_LIBRARY',
          template_id: template.id,
          duration_days: selectedDuration
        })
      });

      if (res.ok) {
        const project = await res.json();
        router.push(`/roadmap/${project.id}`);
      } else {
        router.push('/dashboard');
      }
    } catch (err) {
      router.push('/dashboard');
    } finally {
      setIsStarting(false);
    }
  };

  const filteredTemplates = templates.filter(tmpl => {
    const matchesSearch = tmpl.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
                          tmpl.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          tmpl.tech_stack.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesDiff = selectedDifficulty === 'ALL' || tmpl.difficulty === selectedDifficulty;
    return matchesSearch && matchesDiff;
  });

  return (
    <div id="library-container" className="space-y-8 py-4">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">Built-in Project Library</h1>
          <p className="text-sm text-gray-400">Select a pre-architected functional project template to launch your development timeline.</p>
        </div>
      </div>

      {/* Filter & Search Bar */}
      <div className="glass-card p-4 rounded-2xl flex flex-col md:flex-row gap-4 items-center justify-between">
        <div className="relative w-full md:w-96">
          <Search className="w-4 h-4 text-gray-400 absolute left-3.5 top-3.5" />
          <input
            type="text"
            placeholder="Search projects, tech stack, or tags..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-surface border border-surface-border text-white text-sm focus:outline-none focus:border-indigo-500"
          />
        </div>

        <div className="flex items-center space-x-2 w-full md:w-auto overflow-x-auto">
          {['ALL', 'BEGINNER', 'INTERMEDIATE', 'ADVANCED'].map((diff) => (
            <button
              key={diff}
              onClick={() => setSelectedDifficulty(diff)}
              className={`px-3.5 py-2 rounded-xl text-xs font-semibold transition-all duration-150 ${
                selectedDifficulty === diff 
                  ? 'bg-indigo-600 text-white shadow-md' 
                  : 'bg-surface/80 text-gray-400 hover:text-white border border-surface-border'
              }`}
            >
              {diff}
            </button>
          ))}
        </div>
      </div>

      {/* Templates Grid */}
      <div className="grid md:grid-cols-2 gap-6">
        {filteredTemplates.map((tmpl) => (
          <div key={tmpl.id} className="glass-card p-6 rounded-2xl glass-card-hover space-y-5 flex flex-col justify-between border border-surface-border">
            <div className="space-y-4">
              <div className="flex items-start justify-between">
                <div>
                  <span className={`text-[10px] font-extrabold tracking-wider uppercase px-2.5 py-1 rounded-md border ${
                    tmpl.difficulty === 'BEGINNER' 
                      ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                      : tmpl.difficulty === 'INTERMEDIATE'
                      ? 'bg-purple-500/10 text-purple-400 border-purple-500/30'
                      : 'bg-pink-500/10 text-pink-400 border-pink-500/30'
                  }`}>
                    {tmpl.difficulty}
                  </span>
                  <h3 className="text-xl font-bold text-white mt-2">{tmpl.name}</h3>
                </div>

                <div className="flex items-center space-x-1 text-xs text-gray-400 bg-surface px-2.5 py-1 rounded-lg border border-surface-border">
                  <Clock className="w-3.5 h-3.5 text-indigo-400" />
                  <span>Est. {tmpl.estimated_days} Days</span>
                </div>
              </div>

              <p className="text-xs text-gray-400 leading-relaxed">{tmpl.description}</p>

              {/* Tech Stack Pills */}
              <div className="flex flex-wrap gap-2 pt-1">
                {tmpl.tech_stack.split(',').map((tech, i) => (
                  <span key={i} className="text-[11px] px-2.5 py-1 rounded-lg bg-surface border border-surface-border text-gray-300">
                    {tech.trim()}
                  </span>
                ))}
              </div>
            </div>

            {/* Action Row */}
            <div className="pt-4 border-t border-surface-border flex items-center justify-between gap-4">
              <div className="flex items-center space-x-2">
                <span className="text-xs text-gray-400">Duration:</span>
                <select
                  value={selectedDuration}
                  onChange={(e) => setSelectedDuration(parseInt(e.target.value, 10))}
                  className="bg-surface border border-surface-border text-white text-xs rounded-lg px-2 py-1"
                >
                  <option value={14}>14 Days</option>
                  <option value={30}>30 Days</option>
                  <option value={45}>45 Days</option>
                  <option value={60}>60 Days</option>
                </select>
              </div>

              <button
                id={`start-template-btn-${tmpl.id}`}
                onClick={() => handleStartProject(tmpl)}
                disabled={isStarting}
                className="flex items-center space-x-2 px-4 py-2 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-semibold text-xs shadow-md transition-all duration-150 disabled:opacity-50"
              >
                <span>{isStarting ? 'Launching...' : 'Start Project'}</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
