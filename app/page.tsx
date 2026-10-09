"use client";
import { useState, useEffect } from 'react';
import Link from 'next/link';

// Reusable Anime Card
function AnimeCard({ anime, showProgress }: { anime: any, showProgress?: boolean }) {
  return (
    <Link href={`/anime/${anime.id}`} className="group relative overflow-hidden rounded-lg bg-gray-900 shadow-lg hover:ring-2 hover:ring-purple-500 transition-all block">
      <img
        src={anime.coverImage.large}
        alt={anime.title.romaji}
        className="w-full aspect-[2/3] object-cover group-hover:scale-105 transition-transform duration-300"
      />
      <div className="absolute top-1.5 right-1.5 bg-black/80 text-yellow-400 text-[10px] px-1.5 py-0.5 rounded backdrop-blur-sm">
        ★ {anime.averageScore || 'N/A'}
      </div>
      <div className="absolute top-1.5 left-1.5 bg-purple-900/90 text-purple-200 text-[10px] px-1.5 py-0.5 rounded font-bold uppercase">
        {anime.format}
      </div>
      
      {/* Progress bar for Continue Watching */}
      {showProgress && (
        <div className="absolute bottom-0 left-0 right-0 h-1 bg-gray-800">
          <div className="h-full bg-purple-500" style={{ width: '65%' }}></div>
        </div>
      )}

      <div className="p-2">
        <h3 className="text-xs font-semibold line-clamp-2 leading-tight h-8">
          {anime.title.english || anime.title.romaji}
        </h3>
        <div className="flex flex-wrap gap-1 mt-1">
          {anime.genres?.slice(0, 2).map((g: string) => (
            <span key={g} className="text-[9px] bg-gray-800 text-gray-400 px-1.5 py-0.5 rounded">
              {g}
            </span>
          ))}
        </div>
      </div>
    </Link>
  );
}

// Horizontal Scrolling Row
function Section({ title, animeList, showProgress }: { title: string, animeList: any[], showProgress?: boolean }) {
  if (!animeList || animeList.length === 0) return null;
  return (
    <div className="mb-10">
      <h2 className="text-xl font-bold mb-3 text-purple-300 flex items-center gap-2">{title}</h2>
      <div className="flex overflow-x-auto gap-3 pb-4 snap-x" style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}>
        {animeList.map((a: any) => (
          <div key={a.id} className="w-32 md:w-40 flex-shrink-0 snap-start">
            <AnimeCard anime={a} showProgress={showProgress} />
          </div>
        ))}
      </div>
    </div>
  );
}

export default function Home() {
  const [query, setQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [homeData, setHomeData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  
  // This simulates a logged-in user. Toggle it in the UI to see the difference!
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // Fake data for logged-in sections
  const mockContinueWatching = [
    { id: 21, title: { romaji: "One Piece" }, coverImage: { large: "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx21-ELJzH32cJ69k.jpg" }, averageScore: 88, format: "TV", genres: ["Action", "Adventure"] },
    { id: 16498, title: { romaji: "Attack on Titan" }, coverImage: { large: "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx16498-C6FPmWm59CyP.jpg" }, averageScore: 84, format: "TV", genres: ["Action", "Drama"] },
    { id: 113415, title: { romaji: "Jujutsu Kaisen" }, coverImage: { large: "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx113415-bbBWj4p0s1f6.jpg" }, averageScore: 86, format: "TV", genres: ["Action", "Supernatural"] },
  ];

  const mockWatchlist = [
    { id: 101922, title: { romaji: "Demon Slayer" }, coverImage: { large: "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx101922-WBsBl0ClmgY4.jpg" }, averageScore: 82, format: "TV", genres: ["Action", "Supernatural"] },
    { id: 21459, title: { romaji: "My Hero Academia" }, coverImage: { large: "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx21459-nYbO0zFfQjT1.jpg" }, averageScore: 79, format: "TV", genres: ["Action", "Comedy"] },
  ];

  useEffect(() => {
    const fetchHome = async () => {
      const gql = `
        query {
          trending: Page(page: 1, perPage: 10) { media(type: ANIME, sort: TRENDING_DESC) { id title { romaji english } coverImage { large } averageScore format genres } }
          popular: Page(page: 1, perPage: 10) { media(type: ANIME, sort: POPULARITY_DESC) { id title { romaji english } coverImage { large } averageScore format genres } }
          topRated: Page(page: 1, perPage: 10) { media(type: ANIME, sort: SCORE_DESC) { id title { romaji english } coverImage { large } averageScore format genres } }
          upcoming: Page(page: 1, perPage: 10) { media(type: ANIME, status: NOT_YET_RELEASED, sort: POPULARITY_DESC) { id title { romaji english } coverImage { large } averageScore format genres } }
        }
      `;
      try {
        const res = await fetch('https://graphql.anilist.co', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({ query: gql }),
        });
        const json = await res.json();
        setHomeData(json.data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchHome();
  }, []);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    setSearched(true);

    const gql = `
      query ($search: String) {
        Page(page: 1, perPage: 18) {
          media(type: ANIME, search: $search, sort: POPULARITY_DESC) {
            id title { romaji english } coverImage { large } averageScore format genres
          }
        }
      }
    `;
    try {
      const res = await fetch('https://graphql.anilist.co', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ query: gql, variables: { search: query } }),
      });
      const json = await res.json();
      setSearchResults(json.data.Page.media);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-950 text-white p-4 md:p-8">
      <header className="mb-6 border-b border-gray-800 pb-4 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600">
            🎌 AniPulse
          </h1>
          <p className="text-gray-400 text-sm mt-1">Discover top anime powered by AniList GraphQL</p>
        </div>
        
        {/* Temporary Login Toggle for Testing */}
        <button 
          onClick={() => setIsLoggedIn(!isLoggedIn)}
          className={`text-xs px-3 py-1.5 rounded-full font-bold transition-colors ${isLoggedIn ? 'bg-green-600/20 text-green-400 border border-green-800' : 'bg-gray-800 text-gray-400 border border-gray-700'}`}
        >
          {isLoggedIn ? '✓ Logged In (Demo)' : 'Log In (Demo)'}
        </button>
      </header>

      <form onSubmit={handleSearch} className="flex flex-col sm:flex-row gap-3 mb-8 max-w-2xl">
        <div className="relative flex-1">
          <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500">🔍</span>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search anime (e.g. Solo Leveling, Jujutsu Kaisen)"
            className="w-full bg-gray-900 border border-gray-700 rounded-lg pl-12 pr-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
        </div>
        <button type="submit" className="bg-purple-600 hover:bg-purple-700 px-6 py-3 rounded-lg font-bold transition-colors whitespace-nowrap">
          Search
        </button>
      </form>

      {searched ? (
        <>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-purple-300">🔥 Results for "{query}"</h2>
            <button 
              onClick={() => { setSearched(false); setQuery(''); }} 
              className="text-sm text-gray-400 hover:text-white bg-gray-800 px-3 py-1 rounded"
            >
              ← Back to Home
            </button>
          </div>
          {loading ? (
            <p className="text-center text-purple-400 mt-8">Loading results...</p>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
              {searchResults.map((a: any) => (
                <AnimeCard key={a.id} anime={a} />
              ))}
            </div>
          )}
        </>
      ) : (
        !homeData ? (
          <p className="text-center text-purple-400 mt-8">Loading homepage...</p>
        ) : (
          <>
            {/* LOGGED IN USER SECTIONS (Only visible when logged in) */}
            {isLoggedIn && (
              <Section title="▶️ Continue Watching" animeList={mockContinueWatching} showProgress={true} />
            )}

            <Section title="🔥 Trending Now" animeList={homeData.trending.media} />
            
            {/* LOGGED IN USER SECTIONS (Only visible when logged in) */}
            {isLoggedIn && (
              <Section title="📌 My Watchlist" animeList={mockWatchlist} />
            )}

            <Section title="🌟 Popular All Time" animeList={homeData.popular.media} />
            <Section title="🏆 Top Rated" animeList={homeData.topRated.media} />
            <Section title="🚀 Upcoming Releases" animeList={homeData.upcoming.media} />
          </>
        )
      )}
    </main>
  );
}
