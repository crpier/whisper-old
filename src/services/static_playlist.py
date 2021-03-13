from pathlib import Path
from typing import List

from setup import config

playlist_folder = Path(config.static_playlists_path)


def get_all_static_playlists():
    return [item for item in playlist_folder.iterdir() if item.is_file()]


def get_songs_from_playlist(playlist_name: str):
    playlist_file = playlist_folder.joinpath(playlist_name)
    valid_song_paths: List[Path] = []
    invalid_song_paths: List[Path] = []

    with playlist_file.open('r') as file:
        for song_path_str in file:
            song_path = Path(song_path_str)
            if song_path.exists() and song_path.is_file():
                valid_song_paths.append(song_path)
            else:
                invalid_song_paths.append(song_path)
    return valid_song_paths, invalid_song_paths


def write_playlist(playlist_name: str, songs_paths_str: List[str]):
    # use itertools to optimize
    invalid_song_paths = []
    valid_song_paths = []
    for song_path_str in songs_paths_str:
        song_path = Path(song_path_str)
        if song_path.exists() and song_path.is_file():
            valid_song_paths.append(song_path)
        else:
            invalid_song_paths.append(song_path)
    playlist_file = playlist_folder.joinpath(playlist_name)
    with playlist_file.open('w') as file:
        file.writelines(
            map(lambda x: str(x) + '\n', valid_song_paths)
        )
    return invalid_song_paths
