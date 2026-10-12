import os

detail_code = """'use client';

import { useState, useEffect, use } from 'react';
import Link from 'next/link';

interface StreamingEpisode {
  title: string;
  url: string;
  site: string;
}

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
  streamingEpisodes: StreamingEpisode[];
}

const GRAPHQL_ENDPOINT = 'https://graphql.anilist.co';

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
    streamingEpisodes {
      title
      url
      site
    }
  }
}
`;

export default function AnimeDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params);
  const animeId = parseInt(resolvedParams.id, 10);

  const [anime, setAnime] = useState<AnimeDetails | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedEpisode, setSelectedEpisode] = useState<number>(1);
  const [provider, setProvider] = useState<'vidlink' | 'vidsrc' | 'autoembed'>('vidlink');

  useEffect(() => {
    const fetchDetails = async () => {
      try {
        const res = await fetch(GRAPHQL_ENDPOINT, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          body: JSON.stringify({
            query: DETAILS_QUERY,
            variables: { id: animeId },
          }),
        });

        const json = await res.json();
        if (json.data?.Media) {
          setAnime(json.data.Media);
        }
      } catch (err) {
        console.error('Failed to load anime details:', err);
      } finally {
        setLoading(false);
      }
    };

    if (animeId) {
      fetchDetails();
    }
  }, [animeId]);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-slate-400">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  if (!anime) {
    return (
      <div className="min-h-screen bg-slate-950 text-white p-8 text-center">
        <h2 className="text-xl font-bold">Anime Not Found</h2>
        <Link href="/" className="text-purple-400 underline mt-4 inline-block">
          ← Back to Home
        </Link>
      </div>
    );
  }

  const totalEpisodes = anime.episodes || 12;
  const targetId = anime.idMal || anime.id;

  const getStreamUrl = () => {
    if (provider === 'vidlink') {
      return `https://vidlink.pro/anime/${targetId}/${selectedEpisode}?primaryColor=a855f7&iconColor=a855f7`;
    } else if (provider === 'vidsrc') {
      return `https://vidsrc.me/embed/anime?anilist=${anime.id}&episode=${selectedEpisode}`;
    } else {
      return `https://vidsrc.pro/embed/anime/${targetId}/${selectedEpisode}`;
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 pb-12">
      {/* Banner */}
      <div className="relative h-48 md:h-72 w-full overflow-hidden bg-slate-900 border-b border-slate-800">
        {anime.bannerImage ? (
          <img
            src={anime.bannerImage}
            alt="Banner"
            className="w-full h-full object-cover opacity-40"
          />
        ) : (
          <div className="w-full h-full bg-gradient-to-r from-purple-900/30 to-slate-900" />
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-slate-950 to-transparent" />
      </div>

      {/* Main Content Container */}
      <div className="max-w-4xl mx-auto px-4 -mt-24 relative z-10">
        <Link
          href="/"
          className="inline-flex items-center text-xs font-semibold text-purple-400 hover:text-purple-300 mb-6 bg-slate-900/80 px-3 py-1.5 rounded-lg border border-slate-800 backdrop-blur"
        >
          ← Back to Search
        </Link>

        {/* Dynamic Video Player Section */}
        <div className="mb-8 bg-slate-900 rounded-xl overflow-hidden border border-slate-800 shadow-2xl">
          {/* Server Switcher */}
          <div className="flex bg-slate-950 border-b border-slate-800 p-2 gap-2 text-xs overflow-x-auto">
            <span className="text-slate-400 self-center px-2 font-medium shrink-0">Server:</span>
            <button
              onClick={() => setProvider('vidlink')}
              className={`px-3 py-1.5 rounded font-medium transition-all shrink-0 ${
                provider === 'vidlink' ? 'bg-purple-600 text-white' : 'bg-slate-900 text-slate-400 hover:text-white'
              }`}
            >
              Server 1 (VidLink)
            </button>
            <button
              onClick={() => setProvider('vidsrc')}
              className={`px-3 py-1.5 rounded font-medium transition-all shrink-0 ${
                provider === 'vidsrc' ? 'bg-purple-600 text-white' : 'bg-slate-900 text-slate-400 hover:text-white'
              }`}
            >
              Server 2 (VidSrc Me)
            </button>
            <button
              onClick={() => setProvider('autoembed')}
              className={`px-3 py-1.5 rounded font-medium transition-all shrink-0 ${
                provider === 'autoembed' ? 'bg-purple-600 text-white' : 'bg-slate-900 text-slate-400 hover:text-white'
              }`}
            >
              Server 3 (VidSrc Pro)
            </button>
          </div>

          <div className="relative w-full aspect-video bg-black">
            <iframe
              src={getStreamUrl()}
              className="w-full h-full border-0"
              allowFullScreen
              allow="autoplay; encrypted-media"
              title={`Watching ${anime.title.english || anime.title.romaji} Episode ${selectedEpisode}`}
            />
          </div>

          {/* Episode Buttons Bar */}
          <div className="p-4 border-t border-slate-800">
            <h3 className="text-sm font-bold text-purple-300 mb-3">
              Select Episode (Playing Ep. {selectedEpisode})
            </h3>
            <div className="flex flex-wrap gap-2 max-h-32 overflow-y-auto pr-1">
              {Array.from({ length: totalEpisodes }, (_, i) => i + 1).map((epNum) => (
                <button
                  key={epNum}
                  onClick={() => setSelectedEpisode(epNum)}
                  className={`px-3 py-1.5 rounded text-xs font-semibold transition-all ${
                    selectedEpisode === epNum
                      ? 'bg-purple-600 text-white shadow-lg'
                      : 'bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700'
                  }`}
                >
                  Ep {epNum}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Anime Information Header */}
        <div className="flex flex-col md:flex-row gap-6">
          <img
            src={anime.coverImage.large}
            alt={anime.title.english || anime.title.romaji}
            className="w-48 rounded-xl border-2 border-slate-800 shadow-2xl mx-auto md:mx-0 object-cover"
          />

          <div className="flex-1">
            <h1 className="text-2xl md:text-3xl font-extrabold text-white">
              {anime.title.english || anime.title.romaji}
            </h1>

            <div className="flex items-center gap-4 mt-3 text-sm">
              <span className="text-amber-400 font-bold">
                ★ {anime.averageScore ? `${anime.averageScore}%` : 'N/A'}
              </span>
              <span className="text-slate-400">
                {anime.episodes ? `${anime.episodes} Episodes` : 'Ongoing'}
              </span>
              <span className="bg-purple-950 text-purple-300 px-2 py-0.5 rounded text-xs border border-purple-800">
                {anime.status}
              </span>
            </div>

            <div className="flex flex-wrap gap-2 mt-4">
              {anime.genres.map((g) => (
                <span
                  key={g}
                  className="bg-slate-900 text-purple-300 text-xs px-2.5 py-1 rounded-full border border-slate-800 font-medium"
                >
                  {g}
                </span>
              ))}
            </div>

            <div
              className="mt-6 text-slate-300 text-sm leading-relaxed max-w-none space-y-2"
              dangerouslySetInnerHTML={{
                __html: anime.description || 'No description available.',
              }}
            />
          </div>
        </div>
      </div>
    </main>
  );
}
"""

os.makedirs("app/anime/[id]", exist_ok=True)
with open("app/anime/[id]/page.tsx", "w") as f:
    f.write(detail_code)

print("Updated with fixed embed routes across all servers!")
