from dataclasses import dataclass
from enum import Enum
from pathlib import Path
# from typing import ClassVar, Type, Optional, Any, Mapping
import logging
# from marshmallow import Schema, fields, ValidationError
# from marshmallow_dataclass import dataclass as mdataclass


class Format(Enum):
    mp3 = 'mp3'
    ape = 'ape'
    flac = 'flac'
    ogg = 'ogg'


# Custom fields for validation
# class MMPath(fields.Field):
#     """Field that serializes to a string representing an absolute path,
#     and deserializez to a Path object"""

#     def _serialize(self, value: Path, attr: str, obj: Any, **kwargs):
#         return value.absolute()

#     def _deserialize(
#             self,
#             value: str,
#             attr: Optional[str],
#             data: Optional[Mapping[str, Any]],
#             **kwargs
#     ):
#         deserialized = Path(value)
#         if not deserialized.exists():
#             raise ValidationError(f"field '{attr}' is not an existing path: '{value}'")
#         return Path(value)

# Config class definitions


@dataclass(frozen=True)
class IceConfig:
    password: str
    port: int = 8000
    host: str = 'localhost'
    user: str = 'source'
    format: Format = Format.mp3


@dataclass(frozen=True)
class LoggingConfig:
    filename: str = '/var/log/music_man/main.log'
    level: int = logging.DEBUG


@dataclass(frozen=True)
class DefaultsConfig:
    default_query = 'metallica'
    default_station_name = 'lol'
    default_station_mount = '/angular'
    default_station_genre = 'metal'
    default_station_description = 'This is good music'


# @mdataclass(frozen=True)
# class MainConfig:
#     beets_music_path: Path = field(metadata={
#         'marshmallow_field': MMPath(),
#     })
#     beets_music_db_path: Path = field(metadata={
#         'marshmallow_field': MMPath(),
#     })
#     # When are you going to implement this????
#     static_playlists_path: Path = field(metadata={
#         'marshmallow_field': MMPath(),
#     })
#     log_file: Path = field(
#             default=Path('/var/log/music_man/main.log'),
#             metadata={'marshmallow_field': MMPath()})
#     log_level: int = logging.DEBUG
#     stream_bitrate: int = 4096
#     default_query: str = 'metallica'
#     default_station_name: str = 'lol'
#     default_station_mount: str = '/angular'
#     default_station_genre: str = 'metal'
#     default_station_description: str = 'This is good music'
#     ice_password: str
#     ice_port: int = 8000
#     ice_host: str = 'localhost'
#     ice_user: str = 'source'
#     ice_format: Format = Format.mp3

#     Schema: ClassVar[Type[Schema]] = Schema

# def get_config(config_location: str):
#     config_path = Path(config_location)
#     with config_path.open() as file:
#         raw_config = load(file, Loader=BaseLoader)
#     main_config: Settings = Settings.Schema().load(raw_config)
#     return main_config

from pydantic import BaseSettings


class Settings(BaseSettings):
    beets_music_path: Path
    beets_music_db_path: Path
    # When are you going to implement this????
    static_playlists_path: Path
    log_file: Path
    log_level: int = logging.INFO
    stream_bitrate: int = 4096
    default_query: str = 'metallica'
    default_station_name: str = 'lol'
    default_station_mount: str = '/angular'
    default_station_genre: str = 'metal'
    default_station_description: str = 'This is good music'
    ice_password: str
    ice_port: int = 8000
    ice_host: str = 'localhost'
    ice_user: str = 'source'
    ice_format: Format = Format.mp3

    class Config:
        env_file = ".env"
