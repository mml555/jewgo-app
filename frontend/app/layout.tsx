import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
// import EnvDebug from '@/components/EnvDebug'
// import { ToastContainer } from '@/components/ui/Toast'
// import AuthProvider from '@/components/AuthProvider'
// import ErrorBoundary from '@/components/ui/ErrorBoundary'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Jewgo - Find Your Kosher Eatery',
  description: 'Discover the best kosher restaurants, synagogues, and Jewish businesses in your area.',
  keywords: 'kosher, restaurants, Jewish, eatery, synagogue, mikvah, stores',
  authors: [{ name: 'Jewgo Team' }],
  appleWebApp: {
    capable: true,
    statusBarStyle: 'default',
    title: 'Jewgo',
  },
  other: {
    'mobile-web-app-capable': 'yes',
  },
  formatDetection: {
    telephone: false,
  },
}

export const viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  themeColor: '#A8E6CF',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="h-full">
      <body className={`${inter.className} h-full antialiased`}>
        {/* <ErrorBoundary>
          <AuthProvider> */}
            <div className="min-h-full bg-gray-50 flex flex-col">
              {children}
            </div>
            {/* <ToastContainer />
            {process.env.NODE_ENV === 'development' && <EnvDebug />} */}
          {/* </AuthProvider>
        </ErrorBoundary> */}
      </body>
    </html>
  )
} 