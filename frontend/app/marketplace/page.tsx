'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { 
  Store, 
  Search, 
  Star, 
  GitFork, 
  Clock, 
  ArrowRight, 
  Sparkles, 
  PlusCircle,
  CheckCircle2
} from 'lucide-react';
import { API_BASE } from '../../lib/api';

interface MarketplaceTemplate {
  id: number;
  name: string;
  slug: string;
  description: string;
  difficulty: string;
  category: string;
  tech_stack: string;
  estimated_days: number;
}

export default function MarketplacePage() {
  const router = useRouter();
  const [templates, setTemplates] = useState<MarketplaceTemplate[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [starredIds, setStarredIds] = useState<number[]>([]);
  const [forkingId, setForkingId] = useState<number | null>(null);

  useEffect(() => {
    fetch(`${API_BASE}/api/marketplace/templates`)
      .then(res => res.json())
      .then(data => setTemplates(data))
      .catch(() => {
        setTemplates([
          {
            id: 1,
            name: "Personal Developer Portfolio",
            slug: "personal-portfolio",
            description: "High-performance portfolio with Framer Motion animations & contact API.",
            difficulty: "BEGINNER",
            category: "Frontend",
            tech_stack: "Next.js, TypeScript, Tailwind CSS",
            estimated_days: 14
          },
          {
            id: 2,
            name: "E-Commerce Storefront Platform",
            slug: "ecommerce-platform",
            description: "Full-stack digital store with Stripe checkout and admin dashboard.",
            difficulty: "INTERMEDIATE",
            category: "Fullstack",
            tech_stack: "Next.js, FastAPI, PostgreSQL, Stripe",
            estimated_days: 30
          },
          {
            id: 3,
            name: "Network Intrusion Detection System (IDS)",
            slug: "intrusion-detection-system",
            description: "ML network packet analyzer detecting suspicious traffic anomalies.",
            difficulty: "ADVANCED",
            category: "Security / AI",
            tech_stack: "Python, Scapy, PyTorch, React",
            estimated_days: 60
          }
        ]);
      });
  }, []);

  const handleStar = (id: number) => {
    if (starredIds.includes(id)) {
      setStarredIds(starredIds.filter(i => i !== id));
    } else {
      setStarredIds([...starredIds, id]);
    }
  };

  const handleForkTemplate = async (template: MarketplaceTemplate) => {
    setForkingId(template.id);
    try {
      const res = await fetch(`${API_BASE}/api/projects/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: `${template.name} (Fork)`,
          description: template.description,
          source_type: 'BUILTIN_LIBRARY',
          template_id: template.id,
          duration_days: template.estimated_days
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
      setForkingId(null);
    }
  };

  return (
    <div id="marketplace-container" className="space-y-8 py-4">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight flex items-center gap-3">
            <span>Project Template Marketplace</span>
            <span className="px-3 py-1 rounded-full bg-pink-500/10 border border-pink-500/30 text-pink-400 text-xs font-semibold">
              Community Hub
            </span>
          </h1>
          <p className="text-sm text-gray-400">Discover, star, and fork ready-to-build development project blueprints.</p>
        </div>
      </div>

      {/* Search Bar */}
      <div className="glass-card p-4 rounded-2xl flex items-center justify-between">
        <div className="relative w-full max-w-md">
          <Search className="w-4 h-4 text-gray-400 absolute left-3.5 top-3.5" />
          <input
            type="text"
            placeholder="Search templates by stack or keyword..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-surface border border-surface-border text-white text-sm focus:outline-none focus:border-indigo-500"
          />
        </div>
      </div>

      {/* Grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {templates.map((tmpl) => {
          const isStarred = starredIds.includes(tmpl.id);
          return (
            <div key={tmpl.id} className="glass-card p-6 rounded-2xl glass-card-hover space-y-4 flex flex-col justify-between border border-surface-border">
              <div className="space-y-3">
                <div className="flex items-start justify-between">
                  <span className="text-[10px] font-extrabold px-2.5 py-1 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/30">
                    {tmpl.category}
                  </span>
                  <button
                    onClick={() => handleStar(tmpl.id)}
                    className={`flex items-center space-x-1 text-xs px-2.5 py-1 rounded-lg border transition-colors ${
                      isStarred
                        ? 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                        : 'bg-surface text-gray-400 border-surface-border hover:text-white'
                    }`}
                  >
                    <Star className={`w-3.5 h-3.5 ${isStarred ? 'fill-amber-400 text-amber-400' : ''}`} />
                    <span>{isStarred ? 43 : 42}</span>
                  </button>
                </div>

                <h3 className="font-bold text-white text-lg">{tmpl.name}</h3>
                <p className="text-xs text-gray-400 line-clamp-2">{tmpl.description}</p>
                <div className="text-[11px] text-gray-300 bg-surface/60 px-3 py-1.5 rounded-lg font-mono border border-surface-border">
                  {tmpl.tech_stack}
                </div>
              </div>

              <div className="pt-3 border-t border-surface-border flex items-center justify-between">
                <span className="text-xs text-gray-400 flex items-center gap-1">
                  <Clock className="w-3.5 h-3.5 text-indigo-400" />
                  {tmpl.estimated_days} Days
                </span>

                <button
                  onClick={() => handleForkTemplate(tmpl)}
                  disabled={forkingId === tmpl.id}
                  className="flex items-center space-x-1.5 px-3.5 py-1.5 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-semibold text-xs shadow-md transition-all disabled:opacity-50"
                >
                  <GitFork className="w-3.5 h-3.5" />
                  <span>{forkingId === tmpl.id ? 'Forking...' : 'Fork Template'}</span>
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
