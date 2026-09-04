'use client';

import React, { useEffect, useState } from 'react';
import { 
  Activity, 
  GitCommit, 
  GitBranch, 
  CheckCircle2
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
      setLogs(Array.isArray(logsData) ? logsData : []);
      setCommits(Array.isArray(commitsData) ? commitsData : []);
      setLoading(false);
    });
  }, []);

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
            {loading ? (
              <p className="text-xs text-gray-400 p-4 text-center animate-pulse">Loading commits...</p>
            ) : commits.length === 0 ? (
              <div className="p-8 text-center space-y-2 border border-dashed border-surface-border rounded-2xl">
                <GitCommit className="w-6 h-6 text-gray-500 mx-auto" />
                <p className="text-xs text-gray-400">No GitHub commits pushed yet.</p>
                <p className="text-[11px] text-gray-500">Upload a project ZIP to trigger automated daily git commits.</p>
              </div>
            ) : (
              commits.map((c) => (
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
              ))
            )}
          </div>
        </div>

        {/* Right Column: System Event Stream */}
        <div className="glass-card p-6 rounded-3xl space-y-4 border border-surface-border">
          <div className="flex items-center space-x-2 text-purple-400 font-bold text-base border-b border-surface-border pb-3">
            <Activity className="w-5 h-5 text-purple-400" />
            <span>Execution Audit Trail</span>
          </div>

          <div className="space-y-3">
            {loading ? (
              <p className="text-xs text-gray-400 p-4 text-center animate-pulse">Loading audit trail...</p>
            ) : logs.length === 0 ? (
              <div className="p-8 text-center space-y-2 border border-dashed border-surface-border rounded-2xl">
                <Activity className="w-6 h-6 text-gray-500 mx-auto" />
                <p className="text-xs text-gray-400">No activity logs recorded yet.</p>
                <p className="text-[11px] text-gray-500">System actions and daily milestone executions will appear here.</p>
              </div>
            ) : (
              logs.map((log) => (
                <div key={log.id} className="p-3.5 rounded-xl bg-surface/60 border border-surface-border space-y-1 hover:border-purple-500/30 transition-colors">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 border border-purple-500/30">
                      {log.event_type}
                    </span>
                    <span className="text-[10px] text-gray-500">{new Date(log.created_at).toLocaleDateString()}</span>
                  </div>
                  <p className="text-xs text-gray-300">{log.description}</p>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
