import pytest
from unittest import mock
from typing import List

from beets.library import Item

from services.station import RadioQueue


# Test the Radio Queue class
mocked_logger = mock.MagicMock()

song_titles = [
    "Title 1",
    "Title 2",
    "Title 3",
    "Title 4",
    "Title 5",
    "Title 6",
    "Title 7",
    "Title 8",
    "Title 9",
    "Title 10",
]


song_albums = [
    "Album 1",
    "Album 2",
    "Album 3",
    "Album 4",
    "Album 5",
    "Album 6",
    "Album 7",
    "Album 8",
    "Album 9",
    "Album 10",
]


song_artists = [
    "Artist 1",
    "Artist 2",
    "Artist 3",
    "Artist 4",
    "Artist 5",
    "Artist 6",
    "Artist 7",
    "Artist 8",
    "Artist 9",
    "Artist 10",
]

song_paths = [
    "/path/to/converted/file1",
    "/path/to/converted/file2",
    "/path/to/converted/file3",
    "/path/to/converted/file4",
    "/path/to/converted/file5",
    "/path/to/converted/file6",
    "/path/to/converted/file7",
    "/path/to/converted/file8",
    "/path/to/converted/file9",
    "/path/to/converted/file10",
]


@pytest.fixture
def radio_queue():
    return RadioQueue(mocked_logger)

@pytest.fixture
def songs():
    items = [Item(
        artist=song_artists[i],
        album=song_albums[i],
        title=song_titles[i]) for i in range(10)]
    for i, item in enumerate(items):
        item["alt.radiomusic"] = song_paths[i]
    return items


@pytest.mark.unit
def test_add_to_queue(radio_queue: RadioQueue, songs: List[Item]):
    radio_queue.add_to_queue(songs[1])
    assert radio_queue.get_queue() == [songs[1]]

@pytest.mark.unit
def test_clear_radio_queue(radio_queue: RadioQueue, songs: List[Item]):
    radio_queue.add_to_queue(songs[1])
    radio_queue.clear_radio_queue()

    assert radio_queue.get_queue() == []
