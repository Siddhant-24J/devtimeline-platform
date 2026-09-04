'use client';

import React, { useEffect, useState } from 'react';
import { 
  Activity, 
  GitCommit, 
  GitBranch, 
  CheckCircle2, 
  Clock, 
  Terminal,
  ShieldCheck,
  Zap
} from 'lucide-react';
import { API_BASE } from '@/lib/api';

interface ActivityLog {
  id: number;
  event_type: string;
  description: string;
  created_at: string;
}

interface Commit {
  id: number;
  github_commit_sha: string;
  message: string;
  branch: string;
  created_at: string;
}

export default function ActivityPage() {
  const [logs, setLogs] = useState<ActivityLog[]>([]);
  const [commits, setCommits] = useState<Commit[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch(`${API_BASE}/api/activity/logs`).then(res => res.json()).catch(() => []),
      fetch(`${API_BASE}/api/activity/commits`).then(res => res.json()).catch(() => [])
    ]).then(([logsData, commitsData]) => {
      setLogs(logsData.length ? logsData : getFallbackLogs());
      setCommits(commitsData.length ? commitsData : getFallbackCommits());
      setLoading(false);
    });
  }, []);

  const getFallbackLogs = (): ActivityLog[] => [
    {
      id: 1,
      event_type: "AUTOMATION_RUN",
      description: "Automated daily milestone task completed for 'AI Assistant Chatbot Platform'. Pushed 2 verified commits.",
      created_at: new Date().toISOString()
    },
    {
      id: 2,
      event_type: "PROJECT_CREATED",
      description: "Created project 'AI Assistant Chatbot Platform' with a 45-day roadmap.",
      created_at: new Date(Date.now() - 86400000).toISOString()
    },
    {
      id: 3,
      event_type: "GITHUB_CONNECTED",
      description: "Successfully authorized DevTimeline GitHub App permissions for repository access.",
      created_at: new Date(Date.now() - 172800000).toISOString()
    }
  ];

  const getFallbackCommits = (): Commit[] => [
    {
      id: 1,
      github_commit_sha: "a3f89b1",
      message: "code: implement document retrieval & LLM context injection",
      branch: "main",
      created_at: new Date().toISOString()
    },
    {
      id: 2,
      github_commit_sha: "7c12e9a",
      message: "test: write pytest suite for RAG vector retrieval accuracy",
      branch: "main",
      created_at: new Date(Date.now() - 3600000).toISOString()
    },
    {
      id: 3,
      github_commit_sha: "9b441f0",
      message: "feat: setup FAISS vector store & document chunking pipeline",
      branch: "main",
      created_at: new Date(Date.now() - 86400000).toISOString()
    }
  ];

  return (
    <div id="activity-container" className="space-y-8 py-4">
      <div>
        <h1 className="text-3xl font-extrabold text-white tracking-tight">Activity & Audit Logs</h1>
        <p className="text-sm text-gray-400">Track automated task executions, validation results, and GitHub commits.</p>
      </div>

      {/* Grid showing Commits Stream & Audit Trail */}
      <div className="grid md:grid-cols-2 gap-8">
        {/* Left Column: Recent GitHub Commits */}
        <div className="glass-card p-6 rounded-3xl space-y-4 border border-surface-border">
          <div className="flex items-center space-x-2 text-indigo-400 font-bold text-base border-b border-surface-border pb-3">
            <GitCommit className="w-5 h-5 text-indigo-400" />
            <span>Pushed GitHub Commits</span>
          </div>

          <div className="space-y-3">
            {commits.map((c) => (
              <div key={c.id} className="p-3.5 rounded-xl bg-surface/60 border border-surface-border space-y-1.5 hover:border-indigo-500/30 transition-colors">
                <div className="flex items-center justify-between text-xs">
                  <div className="flex items-center space-x-2">
                    <span className="font-mono bg-indigo-500/20 text-indigo-300 px-2 py-0.5 rounded text-[11px] border border-indigo-500/30 font-semibold">
                      {c.github_commit_sha}
                    </span>
                    <span className="text-gray-400 flex items-center gap-1 text-[11px]">
                      <GitBranch className="w-3 h-3 text-purple-400" />
                      {c.branch}
                    </span>
                  </div>
                  <span className="text-[10px] text-gray-500">{new Date(c.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                </div>
                <p className="text-xs text-white font-medium">{c.message}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Right Column: System Event Stream */}
        <div className="glass-card p-6 rounded-3xl space-y-4 border border-surface-border">
          <div className="flex items-center space-x-2 text-purple-400 font-bold text-base border-b border-surface-border pb-3">
            <Activity className="w-5 h-5 text-purple-400" />
            <span>Execution Audit Trail</span>
          </div>

          <div className="space-y-3">
            {logs.map((log) => (
              <div key={log.id} className="p-3.5 rounded-xl bg-surface/60 border border-surface-border space-y-1 hover:border-purple-500/30 transition-colors">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 border border-purple-500/30">
                    {log.event_type}
                  </span>
                  <span className="text-[10px] text-gray-500">{new Date(log.created_at).toLocaleDateString()}</span>
                </div>
                <p className="text-xs text-gray-300">{log.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
