'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { 
  Github, 
  Award, 
  GitCommit, 
  TrendingUp, 
  CheckCircle2, 
  FolderPlus,
  ExternalLink,
  ShieldCheck,
  Zap,
  Star
} from 'lucide-react';

interface ProfileData {
  username: string;
  avatar_url: string;
  bio: string;
  stats: {
    total_projects: number;
    completed_projects: number;
    total_commits: number;
    streak_days: number;
    rank: string;
  };
  verified_badges: string[];
  showcase_projects: Array<{
    id: number;
    name: string;
    description: string;
    status: string;
    progress_day: string;
  }>;
}

export default function PublicProfilePage() {
  const params = useParams();
  const username = params?.username || 'demo_developer';
  const [profile, setProfile] = useState<ProfileData | null>(null);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/profiles/${username}`)
      .then(res => res.json())
      .then(data => setProfile(data))
      .catch(() => {
        setProfile({
          username: String(username),
          avatar_url: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150",
          bio: "Full-Stack Developer building AI platforms and microservices with DevTimeline.",
          stats: {
            total_projects: 3,
            completed_projects: 1,
            total_commits: 24,
            streak_days: 12,
            rank: "Senior Dev"
          },
          verified_badges: [
            "DevTimeline V1 Pioneer",
            "AI Engine Specialist",
            "Full-Stack Master"
          ],
          showcase_projects: [
            {
              id: 1,
              name: "AI Assistant Chatbot Platform",
              description: "Enterprise RAG AI chatbot platform with document vector search.",
              status: "ACTIVE",
              progress_day: "Day 15 of 45"
            }
          ]
        });
      });
  }, [username]);

  if (!profile) return <div className="text-center p-12 text-gray-400">Loading developer profile...</div>;

  return (
    <div id="developer-profile-container" className="space-y-8 max-w-4xl mx-auto py-4">
      {/* Hero Header Card */}
      <div className="glass-card p-8 rounded-3xl space-y-6 border border-indigo-500/20">
        <div className="flex flex-col md:flex-row items-center md:items-start gap-6 text-center md:text-left">
          <img
            src={profile.avatar_url}
            alt={profile.username}
            className="w-24 h-24 rounded-full border-4 border-indigo-500/40 shadow-xl object-cover"
          />

          <div className="space-y-2">
            <div className="flex items-center justify-center md:justify-start space-x-3">
              <h1 className="text-3xl font-extrabold text-white">@{profile.username}</h1>
              <span className="px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold">
                {profile.stats.rank}
              </span>
            </div>

            <p className="text-xs text-gray-300 max-w-xl">{profile.bio}</p>

            {/* Badges */}
            <div className="flex flex-wrap gap-2 pt-2 justify-center md:justify-start">
              {profile.verified_badges.map((badge, i) => (
                <span key={i} className="flex items-center space-x-1 text-[11px] px-2.5 py-1 rounded-lg bg-purple-500/10 border border-purple-500/30 text-purple-300 font-medium">
                  <ShieldCheck className="w-3.5 h-3.5 text-purple-400" />
                  <span>{badge}</span>
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Stats Row */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-4 border-t border-surface-border">
          <div className="text-center">
            <span className="text-xs text-gray-400 block">Total Projects</span>
            <span className="text-2xl font-bold text-white">{profile.stats.total_projects}</span>
          </div>

          <div className="text-center">
            <span className="text-xs text-gray-400 block">Pushed Commits</span>
            <span className="text-2xl font-bold text-emerald-400">{profile.stats.total_commits}</span>
          </div>

          <div className="text-center">
            <span className="text-xs text-gray-400 block">Current Streak</span>
            <span className="text-2xl font-bold text-pink-400">{profile.stats.streak_days} Days</span>
          </div>

          <div className="text-center">
            <span className="text-xs text-gray-400 block">Verification</span>
            <span className="text-2xl font-bold text-indigo-400">100%</span>
          </div>
        </div>
      </div>

      {/* Projects Showcase */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold text-white">Project Showcase</h2>
        <div className="grid gap-4">
          {profile.showcase_projects.map((proj) => (
            <div key={proj.id} className="glass-card p-6 rounded-2xl flex items-center justify-between border border-surface-border">
              <div className="space-y-1">
                <h3 className="font-bold text-white text-base">{proj.name}</h3>
                <p className="text-xs text-gray-400">{proj.description}</p>
                <span className="text-[11px] text-indigo-400 font-semibold block">{proj.progress_day}</span>
              </div>

              <Link
                href={`/roadmap/${proj.id}`}
                className="px-4 py-2 rounded-xl bg-indigo-600/20 hover:bg-indigo-600/30 text-indigo-300 border border-indigo-500/30 text-xs font-semibold"
              >
                View Roadmap
              </Link>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
