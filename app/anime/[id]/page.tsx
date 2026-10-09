import { fetchAniList } from '@/lib/anilist';
import Link from 'next/link';

const DETAILS_QUERY = `
query ($id: Int) {
  Media(id: $id, type: ANIME) {
    id
    title { romaji english }
    description
    coverImage { large }
    bannerImage
    averageScore
    episodes
    genres
    streamingEpisodes { title url site }
  }
}
`;

export default async function AnimeDetails({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const data = await fetchAniList(DETAILS_QUERY, { id: parseInt(id) });
  const anime = data.Media;

  return (
    <main className="min-h-screen bg-gray-950 text-white">
      {anime.bannerImage && (
        <div className="w-full h-48 md:h-72 overflow-hidden relative">
          <img src={anime.bannerImage} alt="banner" className="w-full h-full object-cover opacity-40" />
          <div className="absolute inset-0 bg-gradient-to-t from-gray-950 to-transparent" />
        </div>
      )}
      
      <div className="p-4 md:p-8 max-w-4xl mx-auto -mt-24 relative z-10">
        <Link href="/" className="text-purple-400 mb-6 inline-block hover:text-purple-300 font-medium">
          ← Back to Home
        </Link>
        
        <div className="flex flex-col md:flex-row gap-6">
          <img src={anime.coverImage.large} alt={anime.title.romaji} className="w-48 rounded-lg shadow-2xl border-2 border-gray-800" />
          
          <div className="flex-1">
            <h1 className="text-3xl md:text-4xl font-bold">{anime.title.english || anime.title.romaji}</h1>
            
            <div className="flex items-center gap-4 mt-3 text-sm">
              <span className="text-yellow-400 font-bold">★ {anime.averageScore || 'N/A'}</span>
              <span className="text-gray-400">{anime.episodes || '?'} Episodes</span>
            </div>
            
            <div className="flex flex-wrap gap-2 mt-4">
              {anime.genres?.map((g: string) => (
                <span key={g} className="bg-purple-900/60 text-purple-200 text-xs px-3 py-1 rounded-full border border-purple-700/50">
                  {g}
                </span>
              ))}
            </div>
            
            <p className="mt-6 text-gray-300 text-sm leading-relaxed" dangerouslySetInnerHTML={{ __html: anime.description }} />
          </div>
        </div>

        {anime.streamingEpisodes?.length > 0 && (
          <div className="mt-10">
            <h2 className="text-xl font-bold mb-4 text-purple-300">🎬 Watch on Official Platforms</h2>
            <div className="grid gap-3">
              {anime.streamingEpisodes.slice(0, 8).map((ep: any, i: number) => (
                <a key={i} href={ep.url} target="_blank" rel="noopener noreferrer" 
                   className="bg-gray-900 hover:bg-gray-800 border border-gray-800 p-4 rounded-lg flex justify-between items-center transition-colors">
                  <span className="text-sm font-medium line-clamp-1">{ep.title}</span>
                  <span className="text-purple-400 text-xs font-bold">{ep.site}</span>
                </a>
              ))}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
