import HomePageClient from '@/components/HomePageClient';
import ErrorBoundary from '@/components/ErrorBoundary';

export default function HomePage() {
  return (
    <ErrorBoundary>
      <HomePageClient />
    </ErrorBoundary>
  );
} 