with open("app/anime/[id]/page.tsx", "r") as f:
    code = f.read()

old_gogo = """            <button
              onClick={() => setProvider('gogo')}
              className={`px-3 py-1.5 rounded font-medium transition-all ${
                provider === 'gogo' ? 'bg-purple-600 text-white' : 'bg-slate-900 text-slate-400 hover:text-white'
              }`}
            >
              Server 2 (Gogo)
            </button>"""

new_gogo = """            <button
              onClick={() => setProvider('vidlink')}
              className={`px-3 py-1.5 rounded font-medium transition-all ${
                provider === 'vidlink' ? 'bg-purple-600 text-white' : 'bg-slate-900 text-slate-400 hover:text-white'
              }`}
            >
              Server 2 (VidLink)
            </button>"""

old_url = "https://iframe.gogo-cdn.com/embed.html?episode=${selectedEpisode}&id=${animeId}"
new_url = "https://vidlink.pro/anime/${animeId}/${selectedEpisode}"

code = code.replace(old_gogo, new_gogo).replace(old_url, new_url)

with open("app/anime/[id]/page.tsx", "w") as f:
    f.write(code)
print("Updated successfully!")
