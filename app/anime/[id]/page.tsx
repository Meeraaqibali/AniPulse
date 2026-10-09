'use client';

import { useState, useEffect, use } from 'react';
import Link from 'next/link';

interface StreamingEpisode {
  title: string;
  url: string;
  site: string;
}

interface AnimeDetails {
  id: number;
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

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-4 -mt-24 relative z-10">
        <Link
          href="/"
          className="inline-flex items-center text-xs font-semibold text-purple-400 hover:text-purple-300 mb-6 bg-slate-900/80 px-3 py-1.5 rounded-lg border border-slate-800 backdrop-blur"
        >
          ← Back to Search
        </Link>

        <div className="flex flex-col md:flex-row gap-6">
          {/* Cover Image */}
          <img
            src={anime.coverImage.large}
            alt={anime.title.english || anime.title.romaji}
            className="w-48 rounded-xl border-2 border-slate-800 shadow-2xl mx-auto md:mx-0 object-cover"
          />

          {/* Details */}
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

            {/* Genre Pills */}
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

            {/* Description */}
            <div
              className="mt-6 text-slate-300 text-sm leading-relaxed max-w-none space-y-2"
              dangerouslySetInnerHTML={{
                __html: anime.description || 'No description available.',
              }}
            />
          </div>
        </div>

        {/* Streaming Platform Section */}
        {anime.streamingEpisodes && anime.streamingEpisodes.length > 0 && (
          <div className="mt-10 pt-6 border-t border-slate-800">
            <h2 className="text-lg font-bold text-purple-300 mb-4 flex items-center gap-2">
              🎬 Watch Official Clips / Episodes
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {anime.streamingEpisodes.slice(0, 6).map((ep, i) => (
                <a
                  key={i}
                  href={ep.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="bg-slate-900 hover:bg-slate-800 border border-slate-800 p-3 rounded-lg flex justify-between items-center text-xs text-slate-200 transition-colors"
                >
                  <span className="font-medium line-clamp-1">{ep.title}</span>
                  <span className="text-purple-400 font-bold ml-2">{ep.site} ↗</span>
                </a>
              ))}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
