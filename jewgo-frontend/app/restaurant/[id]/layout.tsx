// Generate static params for common restaurant IDs
export async function generateStaticParams() {
  // Generate static pages for restaurant IDs 1-50
  // This ensures the build succeeds and creates static pages for common restaurant IDs
  const restaurantIds = Array.from({ length: 50 }, (_, i) => i + 1);
  
  return restaurantIds.map((id) => ({
    id: id.toString(),
  }));
}

export default function RestaurantLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
} 