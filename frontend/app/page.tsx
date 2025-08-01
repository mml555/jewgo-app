import { redirect } from 'next/navigation';

export default function HomePage() {
  // Redirect to the new Eatery explore page
  redirect('/eatery');
} 