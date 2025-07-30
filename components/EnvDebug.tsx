'use client';

import { useEffect, useState } from 'react';

export default function EnvDebug() {
  const [envVars, setEnvVars] = useState<Record<string, string | undefined>>({});
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    
    // Check environment variables
    const vars = {
      NEXT_PUBLIC_GOOGLE_MAPS_API_KEY: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY,
      NODE_ENV: process.env.NODE_ENV,
    };
    
    setEnvVars(vars);
    
    console.log('Environment Variables:', {
      NEXT_PUBLIC_GOOGLE_MAPS_API_KEY: vars.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY ? 'Present' : 'Missing',
      NODE_ENV: vars.NODE_ENV,
    });
  }, []);

  // Don't render anything until mounted to prevent hydration issues
  if (!mounted) {
    return null;
  }

  // Only show in development
  if (envVars.NODE_ENV !== 'development') {
    return null;
  }

  return (
    <div className="fixed top-4 right-4 bg-black text-white p-4 rounded-lg text-xs z-50 max-w-xs">
      <h3 className="font-bold mb-2">Environment Debug</h3>
      <div className="space-y-1">
        <div>
          <strong>NODE_ENV:</strong> {envVars.NODE_ENV || 'undefined'}
        </div>
        <div>
          <strong>API Key:</strong> {envVars.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY ? 'Present' : 'Missing'}
        </div>
      </div>
    </div>
  );
} 