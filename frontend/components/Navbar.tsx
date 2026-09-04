'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  GitBranch, 
  FolderPlus, 
  Store, 
  User, 
  Activity, 
  Settings,
  Sparkles,
  Github
} from 'lucide-react';

export default function Navbar() {
  const pathname = usePathname();

  const navItems = [
    { name: 'Dashboard', href: '/dashboard' },
    { name: 'New Project', href: '/projects/new' },
    { name: 'Library', href: '/library' },
    { name: 'Marketplace', href: '/marketplace' },
    { name: 'Activity Log', href: '/activity' },
    { name: 'Profile', href: '/u/demo_developer' },
    { name: 'Settings', href: '/settings' },
  ];

  return (
    <header className="sticky top-0 z-40 w-full border-b border-surface-border bg-background/80 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Brand Logo */}
        <Link href="/dashboard" className="flex items-center space-x-3 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-purple-600 to-pink-500 flex items-center justify-center shadow-lg group-hover:scale-105 transition-transform duration-200">
            <GitBranch className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center space-x-1.5">
              <span className="text-lg font-extrabold text-white tracking-tight">DevTimeline</span>
              <span className="text-[10px] font-mono uppercase tracking-wider px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                v3.0 Platform
              </span>
            </div>
            <p className="text-[10px] text-gray-400 font-medium hidden sm:block">AI Project Development & GitHub Automation Engine</p>
          </div>
        </Link>

        {/* Desktop Nav Links */}
        <nav className="hidden md:flex items-center space-x-1">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`px-3 py-2 rounded-xl text-xs font-semibold transition-all duration-150 ${
                  isActive
                    ? 'bg-indigo-600 text-white shadow-md'
                    : 'text-gray-400 hover:text-white hover:bg-surface/60'
                }`}
              >
                {item.name}
              </Link>
            );
          })}
        </nav>

        {/* Right Status Indicator */}
        <div className="flex items-center space-x-3">
          <div className="hidden sm:flex items-center space-x-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-medium">
            <Github className="w-3.5 h-3.5" />
            <span>GitHub Connected</span>
          </div>

          <Link
            href="/login"
            className="px-3.5 py-2 rounded-xl bg-surface border border-surface-border text-white text-xs font-semibold hover:border-indigo-500/50 transition-colors"
          >
            Sign In
          </Link>
        </div>
      </div>
    </header>
  );
}
