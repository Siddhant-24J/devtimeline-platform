'use client';

import React, { useState } from 'react';
import { 
  Github, 
  Settings, 
  ShieldCheck, 
  Bell, 
  Cpu, 
  Clock, 
  CheckCircle2,
  Lock
} from 'lucide-react';

export default function SettingsPage() {
  const [saved, setSaved] = useState(false);
  const [defaultDuration, setDefaultDuration] = useState('30');
  const [autoSchedule, setAutoSchedule] = useState('09:00');
  const [aiEnabled, setAiEnabled] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div id="settings-container" className="space-y-8 max-w-4xl mx-auto py-4">
      <div>
        <h1 className="text-3xl font-extrabold text-white tracking-tight">Platform Settings</h1>
        <p className="text-sm text-gray-400">Manage your GitHub App integration, automation schedule, and AI engine preferences.</p>
      </div>

      {saved && (
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-sm flex items-center space-x-2">
          <CheckCircle2 className="w-5 h-5" />
          <span>Configuration saved successfully!</span>
        </div>
      )}

      <form onSubmit={handleSave} className="space-y-6">
        {/* GitHub Account Box */}
        <div className="glass-card p-6 rounded-3xl space-y-4 border border-surface-border">
          <div className="flex items-center space-x-3 text-white font-bold text-lg border-b border-surface-border pb-3">
            <Github className="w-5 h-5 text-emerald-400" />
            <span>GitHub App Connection</span>
          </div>

          <div className="flex items-center justify-between p-4 rounded-2xl bg-surface border border-surface-border">
            <div className="space-y-0.5">
              <span className="font-semibold text-white text-sm block">Authorized GitHub Account</span>
              <span className="text-xs text-gray-400">User: demo_developer • Permissions: Read & Write Repositories</span>
            </div>
            <span className="px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold">
              Connected
            </span>
          </div>
        </div>

        {/* Automation Configuration */}
        <div className="glass-card p-6 rounded-3xl space-y-4 border border-surface-border">
          <div className="flex items-center space-x-3 text-white font-bold text-lg border-b border-surface-border pb-3">
            <Clock className="w-5 h-5 text-indigo-400" />
            <span>Automation & Schedule Defaults</span>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">Default Project Duration</label>
              <select
                value={defaultDuration}
                onChange={(e) => setDefaultDuration(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl bg-surface border border-surface-border text-white text-sm focus:outline-none focus:border-indigo-500"
              >
                <option value="14">14 Days</option>
                <option value="30">30 Days</option>
                <option value="60">60 Days</option>
                <option value="90">90 Days</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-2">Daily Execution Time (UTC)</label>
              <input
                type="time"
                value={autoSchedule}
                onChange={(e) => setAutoSchedule(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl bg-surface border border-surface-border text-white text-sm focus:outline-none focus:border-indigo-500"
              />
            </div>
          </div>
        </div>

        {/* AI Engine Configuration */}
        <div className="glass-card p-6 rounded-3xl space-y-4 border border-surface-border">
          <div className="flex items-center space-x-3 text-white font-bold text-lg border-b border-surface-border pb-3">
            <Cpu className="w-5 h-5 text-purple-400" />
            <span>AI Development Engine (V2 Feature)</span>
          </div>

          <div className="flex items-center justify-between p-4 rounded-2xl bg-surface border border-surface-border">
            <div>
              <span className="font-semibold text-white text-sm block">Enable AI Code Generation Agent</span>
              <span className="text-xs text-gray-400">Allows AI agent to inspect code, write tests, and repair bugs automatically.</span>
            </div>
            <input
              type="checkbox"
              checked={aiEnabled}
              onChange={(e) => setAiEnabled(e.target.checked)}
              className="w-5 h-5 rounded border-surface-border bg-surface text-indigo-600 focus:ring-indigo-500"
            />
          </div>
        </div>

        <button
          type="submit"
          className="px-6 py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-semibold text-sm shadow-lg transition-all duration-150"
        >
          Save Settings
        </button>
      </form>
    </div>
  );
}
