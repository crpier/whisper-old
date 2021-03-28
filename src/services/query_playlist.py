from typing import List

from beets.library import Item

from setup import library

def get_songs_from_query(query: str) -> List[str]:
    items = library.items(query)
    song: Item
    # find a way to ignore errors; TODO maybe beets owner wants types in the code?
    valid_song_paths: List[str] = []
    for song in items:
        song_path = song['alt.radiomusic']
        valid_song_paths.append(song_path)
    return valid_song_paths
