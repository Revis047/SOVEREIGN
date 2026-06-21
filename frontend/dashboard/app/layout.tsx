import './globals.css'

export const metadata = {
  title: 'SOVEREIGN-Ω :: Genesis Terminal',
  description: 'Self-Evolving Autonomous Economic Organism',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-black">{children}</body>
    </html>
  )
}
