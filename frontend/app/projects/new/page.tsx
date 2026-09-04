'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { 
  Upload, 
  Github, 
  BookOpen, 
  Sparkles, 
  ArrowRight, 
  CheckCircle2, 
  Clock, 
  Layers, 
  FolderArchive,
  FileCheck
} from 'lucide-react';
import { API_BASE } from '@/lib/api';

export default function NewProjectPage() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<'zip' | 'github' | 'builtin'>('zip');
  const [loading, setLoading] = useState(false);
  const [githubRepos, setGithubRepos] = useState<any[]>([]);

  // Form Fields
  const [projectName, setProjectName] = useState('');
  const [repositoryName, setRepositoryName] = useState('');
  const [durationDays, setDurationDays] = useState(7);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [selectedTemplateId, setSelectedTemplateId] = useState<number | null>(1);

  useEffect(() => {
    // Fetch GitHub Repos using saved token from localStorage
    const savedToken = typeof window !== 'undefined' ? localStorage.getItem('github_token') : null;
    const url = savedToken ? `${API_BASE}/api/github/repos?token=${savedToken}` : `${API_BASE}/api/github/repos`;

    fetch(url)
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) setGithubRepos(data);
      })
      .catch(() => {});
  }, []);

  const handleZipUploadSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!projectName.trim()) {
      alert('Please enter a project name');
      return;
    }
    if (!selectedFile) {
      alert('Please select a project .zip archive file to upload');
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('name', projectName);
      formData.append('repository_name', repositoryName || `repo-${projectName.toLowerCase().replace(/\s+/g, '-')}`);
      formData.append('duration_days', String(durationDays));

      const res = await fetch(`${API_BASE}/api/projects/upload-zip`, {
        method: 'POST',
        body: formData
      });

      if (res.ok) {
        const project = await res.json();
        router.push(`/roadmap/${project.id}`);
      } else {
        alert('ZIP project decomposition failed. Please verify your ZIP file.');
      }
    } catch (err) {
      alert('Upload error. Falling back to project view.');
      router.push('/dashboard');
    } finally {
      setLoading(false);
    }
  };

  const handleBuiltinSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!projectName.trim()) return;

    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/projects/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: projectName,
          description: `Builtin library project initialized with ${durationDays}-day roadmap.`,
          source_type: 'BUILTIN_LIBRARY',
          template_id: selectedTemplateId,
          duration_days: durationDays,
          repository_name: repositoryName || `repo-${projectName.toLowerCase().replace(/\s+/g, '-')}`
        })
      });

      if (res.ok) {
        const project = await res.json();
        router.push(`/roadmap/${project.id}`);
      }
    } catch (err) {
      router.push('/dashboard');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div id="new-project-container" className="max-w-4xl mx-auto space-y-8 py-4">
      <div>
        <h1 className="text-3xl font-extrabold text-white tracking-tight flex items-center gap-3">
          <span>Create & Decompose Project</span>
          <span className="px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 text-xs font-semibold">
            AI Automated Execution
          </span>
        </h1>
        <p className="text-sm text-gray-400">Upload a project ZIP codebase or choose a blueprint. DevTimeline automatically decomposes it into daily milestones and commits code to your GitHub repo.</p>
      </div>

      {/* Tabs */}
      <div className="flex items-center space-x-2 border-b border-surface-border pb-3">
        {[
          { id: 'zip', label: 'Upload ZIP Codebase', icon: FolderArchive },
          { id: 'github', label: 'Import GitHub Repo', icon: Github },
          { id: 'builtin', label: 'Built-in Blueprint', icon: BookOpen }
        ].map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center space-x-2 px-4 py-2.5 rounded-xl text-xs font-semibold transition-all ${
                activeTab === tab.id
                  ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/30'
                  : 'bg-surface/60 text-gray-400 hover:text-white border border-surface-border'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Tab 1: ZIP Upload & Automated Decomposition */}
      {activeTab === 'zip' && (
        <form onSubmit={handleZipUploadSubmit} className="glass-card p-6 md:p-8 rounded-3xl space-y-6 border border-indigo-500/20">
          <div className="space-y-4">
            <div>
              <label className="text-xs font-bold text-gray-300 block mb-1">Project Name *</label>
              <input
                type="text"
                required
                placeholder="e.g. My Custom SaaS Engine"
                value={projectName}
                onChange={(e) => setProjectName(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-surface border border-surface-border text-white text-sm focus:outline-none focus:border-indigo-500"
              />
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-bold text-gray-300 block mb-1">Target GitHub Repository Name</label>
                <input
                  type="text"
                  placeholder="e.g. my-custom-saas-repo"
                  value={repositoryName}
                  onChange={(e) => setRepositoryName(e.target.value)}
                  className="w-full px-4 py-3 rounded-xl bg-surface border border-surface-border text-white text-sm focus:outline-none focus:border-indigo-500 font-mono"
                />
              </div>

              <div>
                <label className="text-xs font-bold text-gray-300 block mb-1">Upload Duration (Days to Upload on Repo) *</label>
                <select
                  value={durationDays}
                  onChange={(e) => setDurationDays(Number(e.target.value))}
                  className="w-full px-4 py-3 rounded-xl bg-surface border border-surface-border text-white text-sm focus:outline-none focus:border-indigo-500"
                >
                  <option value={7}>7 Days Timeline (1 Week)</option>
                  <option value={14}>14 Days Timeline (2 Weeks)</option>
                  <option value={30}>30 Days Timeline (1 Month)</option>
                  <option value={60}>60 Days Timeline (2 Months)</option>
                </select>
              </div>
            </div>

            {/* Drag & Drop ZIP Zone */}
            <div className="space-y-1">
              <label className="text-xs font-bold text-gray-300 block mb-1">Upload Complete Project (.ZIP File) *</label>
              <div className="border-2 border-dashed border-indigo-500/30 hover:border-indigo-500/60 rounded-2xl p-8 text-center space-y-3 bg-indigo-500/5 transition-all cursor-pointer relative">
                <input
                  type="file"
                  accept=".zip"
                  required
                  onChange={(e) => {
                    if (e.target.files && e.target.files[0]) {
                      setSelectedFile(e.target.files[0]);
                    }
                  }}
                  className="absolute inset-0 opacity-0 cursor-pointer w-full h-full"
                />
                <div className="w-12 h-12 rounded-full bg-indigo-600/20 text-indigo-400 flex items-center justify-center mx-auto">
                  <Upload className="w-6 h-6" />
                </div>
                <div>
                  <p className="text-sm font-bold text-white">
                    {selectedFile ? selectedFile.name : 'Click or Drag & Drop complete project .ZIP file'}
                  </p>
                  <p className="text-xs text-gray-400 mt-1">
                    {selectedFile ? `${(selectedFile.size / (1024 * 1024)).toFixed(2)} MB archive selected` : 'Includes Python, TypeScript, React, Next.js, FastAPI, Node.js codebases'}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 rounded-xl bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:from-indigo-500 hover:to-pink-500 text-white font-bold text-sm shadow-xl transition-all disabled:opacity-50 flex items-center justify-center space-x-2"
          >
            <Sparkles className="w-4 h-4" />
            <span>{loading ? 'Decomposing Codebase & Creating Daily Schedule...' : 'Upload & Decompose Into Daily Git Milestones'}</span>
          </button>
        </form>
      )}

      {/* Tab 2: GitHub Repository Direct Import */}
      {activeTab === 'github' && (
        <div className="glass-card p-6 md:p-8 rounded-3xl space-y-6 border border-surface-border">
          <div className="space-y-3">
            <h3 className="font-bold text-white text-lg">Connected GitHub Repositories</h3>
            <p className="text-xs text-gray-400">Select an existing repository connected to your authenticated GitHub account.</p>
          </div>

          {githubRepos.length > 0 ? (
            <div className="grid gap-3">
              {githubRepos.map((repo) => (
                <div key={repo.id} className="p-4 rounded-xl bg-surface border border-surface-border flex items-center justify-between">
                  <div>
                    <span className="font-bold text-white text-sm block">{repo.name}</span>
                    <span className="text-xs text-gray-400 font-mono">{repo.full_name}</span>
                  </div>
                  <button
                    onClick={() => {
                      setProjectName(repo.name);
                      setRepositoryName(repo.name);
                      setActiveTab('builtin');
                    }}
                    className="px-3.5 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold"
                  >
                    Select Repo
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <div className="p-6 rounded-2xl bg-surface/60 border border-surface-border text-center space-y-2">
              <Github className="w-8 h-8 text-gray-400 mx-auto" />
              <p className="text-xs text-gray-300">No live repos fetched. Click Sign In with GitHub to connect account.</p>
            </div>
          )}
        </div>
      )}

      {/* Tab 3: Built-in Blueprint */}
      {activeTab === 'builtin' && (
        <form onSubmit={handleBuiltinSubmit} className="glass-card p-6 md:p-8 rounded-3xl space-y-6 border border-surface-border">
          <div className="space-y-4">
            <div>
              <label className="text-xs font-bold text-gray-300 block mb-1">Project Name *</label>
              <input
                type="text"
                required
                placeholder="e.g. AI Assistant Chatbot Platform"
                value={projectName}
                onChange={(e) => setProjectName(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-surface border border-surface-border text-white text-sm focus:outline-none focus:border-indigo-500"
              />
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-bold text-gray-300 block mb-1">Duration (Days)</label>
                <input
                  type="number"
                  min={7}
                  max={90}
                  value={durationDays}
                  onChange={(e) => setDurationDays(Number(e.target.value))}
                  className="w-full px-4 py-3 rounded-xl bg-surface border border-surface-border text-white text-sm focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="text-xs font-bold text-gray-300 block mb-1">Target Repository</label>
                <input
                  type="text"
                  placeholder="e.g. ai-chatbot-platform"
                  value={repositoryName}
                  onChange={(e) => setRepositoryName(e.target.value)}
                  className="w-full px-4 py-3 rounded-xl bg-surface border border-surface-border text-white text-sm focus:outline-none focus:border-indigo-500 font-mono"
                />
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-sm shadow-xl transition-all"
          >
            {loading ? 'Generating Roadmap...' : 'Generate Roadmap from Blueprint'}
          </button>
        </form>
      )}
    </div>
  );
}
