import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Document-to-JSON Converter',
  description: 'Upload documents and preview structured JSON in seconds.'
}

export default function RootLayout({
  children
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-slate-50 text-slate-900">
        {children}
      </body>
    </html>
  )
}
