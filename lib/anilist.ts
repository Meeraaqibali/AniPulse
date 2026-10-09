const ANILIST_URL = 'https://graphql.anilist.co';

export async function fetchAniList(query: string, variables = {}) {
  const res = await fetch(ANILIST_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
    body: JSON.stringify({ query, variables }),
    next: { revalidate: 3600 },
  });
  if (!res.ok) throw new Error('AniList request failed');
  const { data } = await res.json();
  return data;
}

export const TRENDING_QUERY = `
query {
  Page(page: 1, perPage: 18) {
    media(type: ANIME, sort: TRENDING_DESC) {
      id
      title { romaji english }
      coverImage { large }
      averageScore
    }
  }
}
`;
