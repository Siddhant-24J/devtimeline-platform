'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  LayoutDashboard, 
  FolderPlus, 
  BookOpen, 
  Map, 
  Activity, 
  Settings, 
  Github,
  Zap
} from 'lucide-react';

export default function Sidebar() {
  const pathname = usePathname();

  const navItems = [
    { label: 'Dashboard', icon: LayoutDashboard, href: '/dashboard', id: 'sidebar-nav-dashboard' },
    { label: 'New Project', icon: FolderPlus, href: '/projects/new', id: 'sidebar-nav-new' },
    { label: 'Project Library', icon: BookOpen, href: '/library', id: 'sidebar-nav-library' },
    { label: 'Activity Logs', icon: Activity, href: '/activity', id: 'sidebar-nav-activity' },
    { label: 'Settings', icon: Settings, href: '/settings', id: 'sidebar-nav-settings' },
  ];

  return (
    <aside id="main-sidebar" className="w-64 h-[calc(100vh-65px)] sticky top-[65px] bg-surface/50 border-r border-surface-border p-4 flex flex-col justify-between hidden md:flex">
      <div className="space-y-6">
        <div>
          <p className="px-3 text-[11px] font-bold tracking-wider text-gray-500 uppercase">Main Navigation</p>
          <nav className="mt-2 space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href || (item.href !== '/' && pathname?.startsWith(item.href));
              
              return (
                <Link
                  key={item.href}
                  id={item.id}
                  href={item.href}
                  className={`flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 ${
                    isActive
                      ? 'bg-indigo-600/20 text-indigo-400 border border-indigo-500/30 font-semibold'
                      : 'text-gray-400 hover:text-gray-200 hover:bg-surface-border/50'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-indigo-400' : 'text-gray-400'}`} />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </nav>
        </div>

        {/* Development Status Box */}
        <div className="p-3.5 rounded-xl bg-gradient-to-b from-indigo-950/40 to-surface border border-indigo-900/30 space-y-2">
          <div className="flex items-center space-x-2 text-xs font-semibold text-indigo-400">
            <Zap className="w-3.5 h-3.5" />
            <span>Automation Engine Active</span>
          </div>
          <p className="text-[11px] text-gray-400 leading-relaxed">
            Daily execution scheduler ready to process project milestones & push GitHub commits.
          </p>
        </div>
      </div>

      {/* Footer Info */}
      <div className="pt-4 border-t border-surface-border text-[11px] text-gray-500 flex items-center justify-between">
        <span>DevTimeline Platform</span>
        <span className="text-gray-400 font-mono">v1.0.0</span>
      </div>
    </aside>
  );
}
