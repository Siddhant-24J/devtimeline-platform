'use client';

import React, { useEffect, useState } from 'react';
import { usePathname, useRouter } from 'next/navigation';

export default function AuthGuard({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [authorized, setAuthorized] = useState(false);

  useEffect(() => {
    // Check for query params from OAuth redirect callback
    const urlParams = new URLSearchParams(window.location.search);
    const tokenParam = urlParams.get('token');
    const userParam = urlParams.get('username');
    const avatarParam = urlParams.get('avatar');

    if (tokenParam) {
      localStorage.setItem('github_token', tokenParam);
    }
    if (userParam) {
      localStorage.setItem('github_user', userParam);
    }
    if (avatarParam) {
      localStorage.setItem('github_avatar', avatarParam);
    }

    const token = localStorage.getItem('github_token');
    const isPublicPage = pathname === '/login';

    if (!token && !isPublicPage) {
      setAuthorized(false);
      router.push('/login');
    } else {
      setAuthorized(true);
    }
  }, [pathname, router]);

  if (!authorized && pathname !== '/login') {
    return (
      <div className="min-h-[70vh] flex flex-col items-center justify-center space-y-4">
        <div className="w-10 h-10 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-sm text-gray-400">Authenticating GitHub session...</p>
      </div>
    );
  }

  return <>{children}</>;
}
