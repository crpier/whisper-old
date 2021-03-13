from typing import List

from beets.library import Item

from setup import library
from util import convert_library_path


def get_songs_from_query(query: str) -> List[str]:
    items = library.items(query)
    song: Item
    valid_song_paths: List[str] = []
    for song in items:
        song_path = convert_library_path(song.path)
        valid_song_paths.append(song_path)
    return valid_song_paths
