'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  GitBranch, 
  User, 
  Github,
  LogOut
} from 'lucide-react';
import { API_BASE } from '@/lib/api';

export default function Navbar() {
  const pathname = usePathname();
  const [username, setUsername] = useState<string | null>(null);
  const [avatar, setAvatar] = useState<string | null>(null);

  useEffect(() => {
    // Check URL params for token & username on OAuth return
    if (typeof window !== 'undefined') {
      const urlParams = new URLSearchParams(window.location.search);
      const tokenParam = urlParams.get('token');
      const userParam = urlParams.get('username');
      const avatarParam = urlParams.get('avatar');

      if (tokenParam) {
        localStorage.setItem('github_token', tokenParam);
      }
      if (userParam) {
        localStorage.setItem('github_user', userParam);
        setUsername(userParam);
      }
      if (avatarParam) {
        localStorage.setItem('github_avatar', avatarParam);
        setAvatar(avatarParam);
      }

      // Read existing storage if set
      const savedUser = localStorage.getItem('github_user');
      const savedAvatar = localStorage.getItem('github_avatar');
      if (savedUser) setUsername(savedUser);
      if (savedAvatar) setAvatar(savedAvatar);
    }
  }, []);

  const handleSignOut = () => {
    localStorage.removeItem('github_token');
    localStorage.removeItem('github_user');
    localStorage.removeItem('github_avatar');
    setUsername(null);
    setAvatar(null);
    window.location.href = '/login';
  };

  const navItems = [
    { name: 'Dashboard', href: '/dashboard' },
    { name: 'New Project', href: '/projects/new' },
    { name: 'Library', href: '/library' },
    { name: 'Marketplace', href: '/marketplace' },
    { name: 'Activity Log', href: '/activity' },
    { name: 'Profile', href: username ? `/u/${username}` : '/u/developer' },
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

        {/* Right Auth Status Bar */}
        <div className="flex items-center space-x-3">
          {username ? (
            <div className="flex items-center space-x-3">
              <div className="flex items-center space-x-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-medium">
                {avatar ? (
                  <img src={avatar} alt={username} className="w-4 h-4 rounded-full" />
                ) : (
                  <Github className="w-3.5 h-3.5" />
                )}
                <span>@{username}</span>
              </div>

              <button
                onClick={handleSignOut}
                title="Sign Out"
                className="p-2 rounded-xl bg-surface border border-surface-border text-gray-400 hover:text-white hover:border-red-500/50 transition-colors"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <a
              href={`${API_BASE}/api/auth/github/login`}
              className="flex items-center space-x-2 px-4 py-2 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white text-xs font-semibold shadow-lg transition-all"
            >
              <Github className="w-4 h-4" />
              <span>Sign In with GitHub</span>
            </a>
          )}
        </div>
      </div>
    </header>
  );
}
