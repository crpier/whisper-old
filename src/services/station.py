import asyncio
import json
import time
from dataclasses import dataclass
from logging import Logger
from queue import Queue, Empty
from threading import Event, Thread
from typing import Union, List

import shout
from beets.library import Item
from broadcaster import Broadcast

from config import IceConfig
from util import convert_library_path, SerializedSong, serialize_song


class RadioQueue:
    def __init__(self, logger):
        self._queue: "Queue[Item]" = Queue()
        self._current_song: Union[Item, None] = None
        self.serialized_queue: List[SerializedSong] = []
        self.logger = logger

    def get_current_song(self):
        return self._current_song

    def get_queue(self) -> List[Item]:
        song_list = list(self._queue.queue)
        return song_list

    def clear_radio_queue(self):
        while not self._queue.empty():
            try:
                self._queue.get(block=False)
            except Empty:
                pass
        self.serialized_queue = []

    def add_to_queue(self, new_item: Item):
        self._queue.put(new_item)
        self.serialized_queue.append(serialize_song(new_item))

    def get_song(self, block=True, timeout=None):
        song = self._queue.get(block=block, timeout=timeout)
        self._current_song = song
        self.serialized_queue.pop(0)
        return song

    def get_serialized_queue(self):
        return self.serialized_queue.copy()


@dataclass
class StreamMetadata:
    name: str = 'Unnamed'
    mount: str = '/stream'
    genre: str = 'De toate....nu manele'
    description: str = 'Indescribable'


class Station:
    def __init__(self,
                 ice_config: IceConfig,
                 bitrate: int,
                 metadata: StreamMetadata,
                 logger: Logger):
        self.player_thread = Thread()

        # Thread events
        self.unpause = Event()
        self.unpause.set()
        self.stopped = Event()
        self.song_skipped = Event()
        self.terminated = Event()

        self.radio_queue = RadioQueue(logger)
        self.logger = logger
        self.metadata = metadata
        logger.debug(f"metadata is {metadata}")

        # Configure shout connection based on config file
        self.shout_connection = shout.Shout()
        self.shout_connection.host = ice_config.host
        self.shout_connection.port = ice_config.port
        self.shout_connection.user = ice_config.user
        self.shout_connection.password = ice_config.password
        self.shout_connection.format = ice_config.format.name
        self.bitrate = bitrate

        # Configure shout connection based on specific parameters
        self.shout_connection.name = metadata.name
        self.shout_connection.mount = metadata.mount
        self.shout_connection.genre = metadata.genre
        self.shout_connection.description = metadata.description

    def pause_playing(self):
        self.unpause.clear()

    def unpause_playing(self):
        self.unpause.set()

    def start_radio(self):
        self.logger.debug(f'starting radio on station {self.metadata.name}')
        self.stopped.clear()
        self.player_thread = Thread(target=self.start_playing,
                                    daemon=True)
        loop = asyncio.new_event_loop()
        self.player_thread.start()

    def stop_radio(self):
        self.stopped.set()

    def skip_song(self):
        self.song_skipped.set()

    def start_playing(self):
        loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)

        loop.run_until_complete(self._start_playing())

    async def _start_playing(self):
        self.logger.debug(f"Using libshout version {shout.version()}")
        self.shout_connection.open()

        broadcast = Broadcast("redis://127.0.0.1:6379")
        await broadcast.connect()

        while not self.terminated.is_set():
            try:
                # TODO log statement should show which station
                self.logger.debug(f'extracting from queue')
                song: Item = self.radio_queue.get_song(timeout=0.5)
                self._current_song = song
                new_status = {
                    self.metadata.name: {
                        'now_playing': f'{song.title} - {song.album} - {song.artist}'
                    }
                }
                await broadcast.publish('song_change', json.dumps(new_status))
                self.logger.debug(f'got from queue: {song.title} - {song.album}')
            except Empty:
                if not self.stopped.is_set():
                    # no timeout, stay here until we get a new song
                    song: Item = self.radio_queue.get_song()
                else:
                    self.logger.debug('Stream has been stopped. Bye bye')
                    self.shout_connection.close()
                    break
            song_path = convert_library_path(self._current_song.path)
            with open(song_path, 'rb') as music_file:
                self.logger.debug(f'opened: {str(song_path)}')
                self.shout_connection.set_metadata({'song': song.title,
                                                    'album': song.album})
                total = 0
                st = time.time()

                nbuf = music_file.read(self.bitrate)
                self.song_skipped.clear()
                while self.unpause.wait() and not self.stopped.is_set() and not self.song_skipped.is_set():
                    buf = nbuf
                    nbuf = music_file.read(self.bitrate)
                    total = total + len(buf)
                    if len(buf) == 0:
                        self.logger.debug(f'buffer is empty, out')
                        break
                    try:
                        self.shout_connection.send(buf)
                        self.shout_connection.sync()
                    except shout.ShoutException as e:
                        self.logger.debug(f'Connection timeout. Reopening socket {self.shout_connection}')
                        self.shout_connection.close()
                        self.shout_connection.open()
                        self.shout_connection.send(buf)
                        self.shout_connection.sync()
                et = time.time()
                br = total * 0.008 / (et - st)
                self.logger.debug("Sent %d bytes in %d seconds (%f kbps)" % (total, et - st, br))
        self.shout_connection.close()


class StationContainer:
    def __init__(self,
                 ice_config: IceConfig,
                 bitrate: int,
                 logger):
        self.__container = {}
        self.ice_config = ice_config
        self.bitrate = bitrate
        self.logger = logger

    def get_container_status(self):
        container_status = {}
        stations = self.__container.values()
        station: Station
        for station in stations:
            station_status = {
                'mount': station.metadata.mount,
                'description': station.metadata.description,
                'genre': station.metadata.genre,
                'now_playing': f'{station._current_song.title} - {station._current_song.album} - {station._current_song.artist}',
                'name': station.metadata.name
            }
            container_status.update({station.metadata.name: station_status})
        return container_status

    def get_station(self, name: str) -> Station:
        # TODO custom exception like below
        return self.__container[name]

    def create_station(self, metadata: StreamMetadata):
        if self.__container.get(metadata.name) is not None:
            # TODO this doesn't do what I wanted, I thought it would raise the exception to the fastapi exceptionhandler and show it there
            raise StationExistsException()
        new_station = Station(self.ice_config, self.bitrate, metadata, self.logger)
        self.__container[metadata.name] = new_station
        return new_station

    async def remove_station(self, name: str):
        station_to_remove: Station = self.__container.get(name)
        if station_to_remove is None:
            raise StationNonexistentException

        station_to_remove.terminated.set()
        station_to_remove.stopped.set()
        station_to_remove.player_thread.join()
        broadcast = Broadcast("redis://127.0.0.1:6379")
        await broadcast.connect()
        await broadcast.publish('song_change', 'aaa')
        del self.__container[name]


class StationExistsException(Exception):
    pass


class StationNonexistentException(Exception):
    pass
