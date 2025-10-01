/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  
  // Environment variables for production
  env: {
    NEXT_PUBLIC_API_URL: process.env.NODE_ENV === 'production' 
      ? '/api' 
      : 'http://localhost:8000',
    NEXT_PUBLIC_WS_URL: process.env.NODE_ENV === 'production'
      ? `wss://${process.env.VERCEL_URL || 'localhost'}/api`
      : 'ws://localhost:8000',
  },

  // Vercel deployment configuration
  async rewrites() {
    if (process.env.NODE_ENV === 'development') {
      return [
        {
          source: '/api/:path*',
          destination: 'http://localhost:8000/:path*',
        },
      ];
    }
    return [];
  },

  // Optimize for serverless deployment
  experimental: {
    outputFileTracingRoot: process.cwd(),
  },
}

module.exports = nextConfig