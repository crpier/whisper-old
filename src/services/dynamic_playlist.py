# TODO maybe give this up?
from typing import List

from beets.library import Item

from setup import library


def get_songs_list() -> List[Item]:
    # empty query so we get all music in the library
    items = list(library.items(""))
    return items
