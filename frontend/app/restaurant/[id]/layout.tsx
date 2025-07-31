import { Metadata } from 'next'

interface RestaurantLayoutProps {
  children: React.ReactNode
  params: { id: string }
}

export async function generateMetadata({ params }: { params: { id: string } }): Promise<Metadata> {
  try {
    // Fetch restaurant data for metadata
    const apiUrl = process.env.NEXT_PUBLIC_BACKEND_URL 
      ? `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/restaurants`
      : process.env.NODE_ENV === 'production'
      ? 'https://jewgo.onrender.com/api/restaurants'
      : 'http://127.0.0.1:8081/api/restaurants'
    
    const response = await fetch(`${apiUrl}/${params.id}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      return {
        title: 'Restaurant Not Found - Jewgo',
        description: 'The requested restaurant could not be found.',
      }
    }

    const data = await response.json()
    const restaurant = data.restaurant || data

    if (!restaurant) {
      return {
        title: 'Restaurant Not Found - Jewgo',
        description: 'The requested restaurant could not be found.',
      }
    }

    const title = `${restaurant.name} - Kosher Restaurant | Jewgo`
    const description = restaurant.short_description 
      ? `${restaurant.short_description} ${restaurant.address ? `Located in ${restaurant.address}.` : ''}`
      : `Visit ${restaurant.name}, a kosher restaurant${restaurant.address ? ` in ${restaurant.address}` : ''}. ${restaurant.certifying_agency ? `Certified by ${restaurant.certifying_agency}.` : ''}`
    
    const imageUrl = restaurant.image_url || 'https://jewgo.com/og-image.jpg'

    return {
      title,
      description,
      keywords: `kosher restaurant, ${restaurant.name}, ${restaurant.kosher_category || 'kosher food'}, ${restaurant.certifying_agency || 'kosher certification'}, Jewish restaurant, kosher dining`,
      openGraph: {
        type: 'website',
        title,
        description,
        url: `https://jewgo.com/restaurant/${params.id}`,
        siteName: 'Jewgo',
        images: [
          {
            url: imageUrl,
            width: 1200,
            height: 630,
            alt: restaurant.name,
          },
        ],
        locale: 'en_US',
      },
      twitter: {
        card: 'summary_large_image',
        title,
        description,
        images: [imageUrl],
        creator: '@jewgoapp',
      },
      robots: {
        index: true,
        follow: true,
        googleBot: {
          index: true,
          follow: true,
          'max-video-preview': -1,
          'max-image-preview': 'large',
          'max-snippet': -1,
        },
      },
    }
  } catch (error) {
    console.error('Error generating restaurant metadata:', error)
    return {
      title: 'Restaurant - Jewgo',
      description: 'Kosher restaurant information on Jewgo.',
    }
  }
}

export default function RestaurantLayout({ children }: RestaurantLayoutProps) {
  return children
} 