from mutagen.mp3 import MP3
from pathlib import Path
from fuzzywuzzy import fuzz

# per ID3: https://en.wikipedia.org/wiki/ID3
TITLE = 'TIT2'
ARTIST = 'TPE1'

song_db = {}

def resolve_tag(tag):
    if len(tag) == 0:
        return None
    text = tag[0].text
    if len(text) == 0:
        return None
    return text[0]

print("Initializing songs db")
for path in Path('data').rglob('*.mp3'):
    mp3 = MP3(path.resolve())
    title = resolve_tag(mp3.tags.getall(TITLE))
    artist = resolve_tag(mp3.tags.getall(ARTIST))
    if title and artist:
        song_db[(title, artist)] = path.resolve()

def search_songs(query):
    query = query.lower()
    max_title_score, max_artist_score = 0, 0
    closest_by_title, closest_by_artist = None, None
    for title, artist in song_db:
        path = song_db[(title, artist)]
        title_score, artist_score = fuzz.partial_ratio(query, title.lower()), \
            fuzz.partial_ratio(query, artist.lower())
        if title_score > max_title_score:
            closest_by_title, max_title_score = (title, artist), title_score
        if artist_score > max_artist_score:
            closest_by_artist, max_artist_score = (title, artist), artist_score

    if (max_title_score >= max_artist_score):
        return closest_by_title + (song_db[closest_by_title],)
    return closest_by_artist + (song_db[closest_by_artist],)

search_songs("BAD BOY")
