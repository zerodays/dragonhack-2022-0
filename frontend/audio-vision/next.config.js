/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['cdn.arstechnica.net', 'i.imgur.com']
  }
}

module.exports = nextConfig
