import os

code = '''\'use client\';

import { useState, useEffect } from \'react\';
import Link from \'next/link\';

interface AnimeDetails {
  id: number;
  idMal: number | null;
  title: {
    english: string | null;
    romaji: string;
  };
  description: string | null;
  bannerImage: string | null;
  coverImage: {
    large: string;
  };
  averageScore: number | null;
  episodes: number | null;
  genres: string[];
  status: string;
}

interface RecommendedAnime {
  id: number;
  title: {
    english: string | null;
    romaji: string;
  };
  coverImage: {
    large: string;
  };
  averageScore: number | null;
  episodes: number | null;
}

const GRAPHQL_ENDPOINT = \'https://graphql.anilist.co\';

const DETAILS_QUERY = `
query ($id: Int) {
  Media(id: $id, type: ANIME) {
    id
    idMal
    title {
      romaji
      english
    }
    description
    coverImage {
      large
    }
    bannerImage
    averageScore
    episodes
    status
    genres
  }
  Page(page: 1, perPage: 10) {
    media(type: ANIME, sort: POPULARITY_DESC) {
      id
      title {
        romaji
        english
      }
      coverImage {
        large
      }
      averageScore
      episodes
    }
  }
}
`;

export default function AnimeDetailPage({ params }: { params: { id: string } | Promise<{ id: string }> }) {
  const [resolvedId, setResolvedId] = useState<number | null>(null);
  const [anime, setAnime] = useState<AnimeDetails | null>(null);
  const [recommendations, setRecommendations] = useState<RecommendedAnime[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedEpisode, setSelectedEpisode] = useState<number>(1);
  const [server, setServer] = useState<'server1' | 'server2' | 'server3'>('server1');

  useEffect(() => {
    Promise.resolve(params).then((p) => {
      const parsedId = parseInt(p.id, 10);
      if (!isNaN(parsedId)) {
        setResolvedId(parsedId);
      } else {
        setLoading(false);
      }
    });
  }, [params]);

  useEffect(() => {
    if (!resolvedId) return;

    let isMounted = true;
    const fetchDetails = async () => {
      const timer = setTimeout(() => {
        if (isMounted) setLoading(false);
      }, 3000);

      try {
        const res = await fetch(GRAPHQL_ENDPOINT, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          body: JSON.stringify({
            query: DETAILS_QUERY,
            variables: { id: resolvedId },
          }),
        });

        const json = await res.json();
        if (isMounted) {
          if (json.data?.Media) {
            setAnime(json.data.Media);
          }
          if (json.data?.Page?.media) {
            const filtered = json.data.Page.media.filter((item: RecommendedAnime) => item.id !== resolvedId);
            setRecommendations(filtered);
          }
        }
      } catch (err) {
        console.error('Failed to load anime details:', err);
      } finally {
        clearTimeout(timer);
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    fetchDetails();

    return () => {
      isMounted = false;
    };
  }, [resolvedId]);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center text-slate-400 gap-4">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500"></div>
        <p className="text-sm font-medium tracking-wider">LOADING ANIPULSE...</p>
      </div>
    );
  }

  if (!anime) {
    return (
      <div className="min-h-screen bg-slate-950 text-white p-8 text-center flex flex-col items-center justify-center">
        <h2 className="text-2xl font-bold mb-2">Anime Not Found</h2>
        <p className="text-slate-400 text-sm mb-6">The requested series could not be loaded.</p>
        <Link href="/" className="bg-purple-600 hover:bg-purple-500 text-white px-6 py-2.5 rounded-xl font-semibold transition-all shadow-lg shadow-purple-600/30">
          ← Back to Home
        </Link>
      </div>
    );
  }

  const totalEpisodes = anime.episodes || 24;

  const getStreamUrl = () => {
    const malId = anime.idMal || anime.id;
    if (server === 'server1') {
      return `https://vidlink.pro/anime/${malId}/${selectedEpisode}?primaryColor=a855f7`;
    } else if (server === 'server2') {
      return `https://vidsrc.me/embed/anime?anilist=${anime.id}&episode=${selectedEpisode}`;
    } else {
      return `https://vidsrc.cc/v2/embed/anime/${anime.id}/${selectedEpisode}`;
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 pb-16">
      {/* Cinematic Banner */}
      <div className="relative h-64 md:h-96 w-full overflow-hidden bg-slate-900 border-b border-slate-800/80">
        {anime.bannerImage ? (
          <img
            src={anime.bannerImage}
            alt="Banner"
            className="w-full h-full object-cover opacity-35 scale-105 transform"
          />
        ) : (
          <div className="w-full h-full bg-gradient-to-r from-purple-950/40 via-slate-900 to-slate-950" />
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/40 to-transparent" />
        
        <div className="absolute top-6 left-6 z-20">
          <Link
            href="/"
            className="inline-flex items-center text-xs font-bold text-white bg-slate-900/80 hover:bg-purple-600 px-4 py-2 rounded-xl border border-slate-700/60 backdrop-blur-md transition-all shadow-lg"
          >
            ← Back to Home
          </Link>
        </div>
      </div>

      {/* Main Content Layout */}
      <div className="max-w-6xl mx-auto px-4 sm:px-6 -mt-32 md:-mt-44 relative z-10">
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Left Column: Poster & Stats */}
          <div className="lg:col-span-1 flex flex-col items-center lg:items-start gap-4">
            <div className="w-48 sm:w-56 rounded-2xl overflow-hidden border-2 border-slate-800/80 shadow-2xl bg-slate-900">
              <img
                src={anime.coverImage.large}
                alt={anime.title.english || anime.title.romaji}
                className="w-full h-auto object-cover aspect-[3/4]"
              />
            </div>

            <div className="w-full bg-slate-900/90 border border-slate-800/80 rounded-2xl p-4 backdrop-blur-md shadow-xl space-y-3">
              <div className="flex justify-between items-center text-sm">
                <span className="text-slate-400 font-medium">Score</span>
                <span className="text-amber-400 font-extrabold flex items-center gap-1">
                  ★ {anime.averageScore ? `${anime.averageScore}%` : 'N/A'}
                </span>
              </div>
              <div className="h-px bg-slate-800" />
              <div className="flex justify-between items-center text-sm">
                <span className="text-slate-400 font-medium">Episodes</span>
                <span className="text-slate-200 font-bold">{anime.episodes || 'Ongoing'}</span>
              </div>
              <div className="h-px bg-slate-800" />
              <div className="flex justify-between items-center text-sm">
                <span className="text-slate-400 font-medium">Status</span>
                <span className="bg-purple-950/80 text-purple-300 px-2.5 py-0.5 rounded-full text-xs font-semibold border border-purple-800/50">
                  {anime.status}
                </span>
              </div>
            </div>
          </div>

          {/* Right Column: Title, Description & Video Player */}
          <div className="lg:col-span-2 flex flex-col gap-6">
            <div>
              <h1 className="text-3xl sm:text-4xl font-black text-white tracking-tight drop-shadow-md">
                {anime.title.english || anime.title.romaji}
              </h1>

              <div className="flex flex-wrap gap-2 mt-3">
                {anime.genres.map((g) => (
                  <span
                    key={g}
                    className="bg-purple-950/60 text-purple-300 text-xs px-3 py-1 rounded-full border border-purple-800/40 font-semibold"
                  >
                    {g}
                  </span>
                ))}
              </div>

              <div
                className="mt-4 text-slate-300 text-sm sm:text-base leading-relaxed space-y-2 bg-slate-900/50 p-4 rounded-2xl border border-slate-800/60 backdrop-blur-sm"
                dangerouslySetInnerHTML={{
                  __html: anime.description || 'No description available.',
                }}
              />
            </div>

            {/* Premium Video Player Container */}
            <div className="bg-slate-900 rounded-2xl overflow-hidden border border-slate-800/80 shadow-2xl">
              
              {/* Server Switcher Bar */}
              <div className="flex justify-between items-center bg-slate-950/90 border-b border-slate-800 px-4 py-3 gap-2 flex-wrap">
                <div className="flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-purple-500 animate-pulse"></span>
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-300">Servers</span>
                </div>
                <div className="flex gap-2 flex-wrap">
                  <button
                    onClick={() => setServer('server1')}
                    className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all shadow-md ${
                      server === 'server1' ? 'bg-purple-600 text-white shadow-purple-600/30' : 'bg-slate-900 hover:bg-slate-800 text-slate-400 border border-slate-800'
                    }`}
                  >
                    Server 1 (VidLink)
                  </button>
                  <button
                    onClick={() => setServer('server2')}
                    className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all shadow-md ${
                      server === 'server2' ? 'bg-purple-600 text-white shadow-purple-600/30' : 'bg-slate-900 hover:bg-slate-800 text-slate-400 border border-slate-800'
                    }`}
                  >
                    Server 2 (VidSrc Me)
                  </button>
                  <button
                    onClick={() => setServer('server3')}
                    className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all shadow-md ${
                      server === 'server3' ? 'bg-purple-600 text-white shadow-purple-600/30' : 'bg-slate-900 hover:bg-slate-800 text-slate-400 border border-slate-800'
                    }`}
                  >
                    Server 3 (VidSrc CC)
                  </button>
                </div>
              </div>

              {/* Video Screen Frame */}
              <div className="relative w-full aspect-video bg-black flex items-center justify-center">
                <iframe
                  src={getStreamUrl()}
                  className="w-full h-full border-0"
                  allowFullScreen
                  allow="autoplay; encrypted-media"
                  title={`Watching Episode ${selectedEpisode}`}
                />
              </div>

              {/* Episode Selector Tray */}
              <div className="p-5 border-top border-slate-800/80 bg-slate-900/90">
                <div className="flex justify-between items-center mb-3">
                  <h3 className="text-sm font-bold text-purple-300 uppercase tracking-wide">
                    Episodes <span className="text-slate-400 font-normal normal-case">(Playing Ep. {selectedEpisode})</span>
                  </h3>
                  <span className="text-xs text-slate-400 font-medium">{totalEpisodes} Episodes Available</span>
                </div>
                <div className="flex flex-wrap gap-2 max-h-40 overflow-y-auto pr-2">
                  {Array.from({ length: totalEpisodes }, (_, i) => i + 1).map((epNum) => (
                    <button
                      key={epNum}
                      onClick={() => setSelectedEpisode(epNum)}
                      className={`w-11 h-11 rounded-xl text-xs font-bold transition-all flex items-center justify-center shadow-md ${
                        selectedEpisode === epNum
                          ? 'bg-purple-600 text-white ring-2 ring-purple-400/50 shadow-purple-600/40 scale-105'
                          : 'bg-slate-800/90 hover:bg-slate-700 text-slate-300 border border-slate-700/60'
                      }`}
                    >
                      {epNum}
                    </button>
                  ))}
                </div>
              </div>

            </div>

          </div>

        </div>

        {/* Suggested / Recommended Series Section */}
        <div className="mt-16">
          <div className="flex items-center justify-between mb-6 border-b border-slate-800/80 pb-4">
            <h2 className="text-xl sm:text-2xl font-extrabold text-white flex items-center gap-2">
              <span className="text-purple-500">⚡</span> You May Also Like
            </h2>
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-widest">Trending Picks</span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 sm:gap-6">
            {recommendations.map((rec) => (
              <Link
                key={rec.id}
                href={`/anime/${rec.id}`}
                className="group bg-slate-900/90 rounded-2xl overflow-hidden border border-slate-800/80 hover:border-purple-500/60 transition-all duration-300 shadow-xl flex flex-col"
              >
                <div className="relative aspect-[3/4] overflow-hidden bg-slate-950">
                  <img
                    src={rec.coverImage.large}
                    alt={rec.title.english || rec.title.romaji}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                  {rec.averageScore && (
                    <span className="absolute top-2.5 right-2.5 bg-slate-950/85 text-amber-400 font-extrabold text-xs px-2.5 py-1 rounded-lg backdrop-blur-md border border-slate-800 shadow-lg">
                      ★ {rec.averageScore}%
                    </span>
                  )}
                </div>
                <div className="p-3.5 flex flex-col justify-between flex-1">
                  <h3 className="font-bold text-sm text-slate-100 line-clamp-1 group-hover:text-purple-400 transition-colors">
                    {rec.title.english || rec.title.romaji}
                  </h3>
                  <p className="text-xs text-slate-400 mt-1 font-medium">
                    {rec.episodes ? `${rec.episodes} Episodes` : 'Ongoing Series'}
                  </p>
                </div>
              </Link>
            ))}
          </div>
        </div>

      </div>
    </main>
  );
}
'''

os.makedirs('app/anime/[id]', exist_ok=True)
with open('app/anime/[id]/page.tsx', 'w') as f:
    f.write(code)

print('File written successfully without history errors!')
