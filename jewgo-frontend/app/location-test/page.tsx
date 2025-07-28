import LocationSearchTest from '@/components/LocationSearchTest';
import GoogleMapsLoader from '@/components/GoogleMapsLoader';

export default function LocationTestPage() {
  return (
    <GoogleMapsLoader>
      <LocationSearchTest />
    </GoogleMapsLoader>
  );
} 