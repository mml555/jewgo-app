import { Suspense } from 'react';
import LiveMapClient from '@/components/LiveMapClient';

export default function LiveMapPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-gray-500">Loading map...</div>
    </div>}>
      <LiveMapClient />
    </Suspense>
  );
} 