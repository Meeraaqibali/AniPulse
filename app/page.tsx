import { fetchAniList, TRENDING_QUERY } from '@/lib/anilist';
import Link from 'next/link';

export default async function Home() {
  const data = await fetchAniList(TRENDING_QUERY);
  const anime = data.Page.media;

  return (
    <main className="min-h-screen bg-gray-950 text-white p-4 md:p-8">
      <header className="mb-8 border-b border-gray-800 pb-4">
        <h1 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600">
          🎌 AniPulse
        </h1>
        <p className="text-gray-400 text-sm mt-1">Discover your next favorite anime</p>
      </header>

      <h2 className="text-xl font-bold mb-4 text-purple-300">🔥 Trending Now</h2>
      
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
        {anime.map((a: any) => (
          <Link href={`/anime/${a.id}`} key={a.id} className="group relative overflow-hidden rounded-lg bg-gray-900 shadow-lg hover:ring-2 hover:ring-purple-500 transition-all">
            <img
              src={a.coverImage.large}
              alt={a.title.romaji}
              className="w-full aspect-[2/3] object-cover group-hover:scale-105 transition-transform duration-300"
            />
            <div className="absolute top-2 right-2 bg-black/80 text-yellow-400 text-xs px-2 py-1 rounded backdrop-blur-sm">
              ★ {a.averageScore || 'N/A'}
            </div>
            <div className="p-3 bg-gradient-to-t from-gray-900 to-transparent">
              <h3 className="text-sm font-semibold line-clamp-2 leading-tight">
                {a.title.english || a.title.romaji}
              </h3>
            </div>
          </Link>
        ))}
      </div>
    </main>
  );
}
