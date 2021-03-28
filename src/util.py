import collections
import re
from pathlib import Path

from beets.library import Item


def update_status(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update_status(d.get(k, {}), v)
        else:
            d[k] = v
    return d


class SerializedSong:
    album: str
    id: str
    title: str
    artist: str
    genre: str
    path: Path

    def __init__(self, song: Item):
        self.album = song.album
        self.id = song.id
        self.title = song.title
        self.artist = song.artist
        self.genre = song.genre
        self.path = Path(song['alt.radiomusic'])


def serialize_song(song: Item) -> SerializedSong:
    serialized = SerializedSong(song)
    return serialized
