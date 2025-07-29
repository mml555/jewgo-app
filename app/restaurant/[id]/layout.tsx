// Generate static params for common restaurant IDs
export async function generateStaticParams() {
  // Generate static pages for restaurant IDs 1-300
  // This ensures the build succeeds and creates static pages for a wider range of restaurant IDs
  const restaurantIds = Array.from({ length: 300 }, (_, i) => i + 1);
  
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