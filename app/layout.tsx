import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Link from "next/link";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AniPulse",
  description: "Discover your next favorite anime",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-gray-950 text-white`}>
        {/* Navigation Bar */}
        <header className="sticky top-0 z-50 bg-gray-900/80 backdrop-blur-md border-b border-gray-800 px-4 py-3 flex justify-between items-center">
          <Link href="/" className="text-xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600">
            🎌 AniPulse
          </Link>
          <div className="flex items-center gap-4 text-xl">
            <Link href="/settings" className="hover:scale-110 transition-transform" title="Settings">
              ⚙️
            </Link>
            <Link href="/profile" className="hover:scale-110 transition-transform" title="Profile">
              👤
            </Link>
          </div>
        </header>
        
        {children}
      </body>
    </html>
  );
}
