from dataclasses import field, dataclass
from enum import Enum
from pathlib import Path
from typing import ClassVar, Type, Optional, Any, Mapping
import logging
from marshmallow import Schema, fields, ValidationError
from marshmallow_dataclass import dataclass as mdataclass
from yaml import load, BaseLoader

class Format(Enum):
    mp3 = 'mp3'
    ape = 'ape'
    flac = 'flac'
    ogg = 'ogg'

# Custom fields for validation
class MMPath(fields.Field):
    """Field that serializes to a string representing an absolute path,
    and deserializez to a Path object"""

    def _serialize(self, value: Path, attr: str, obj: Any, **kwargs):
        return value.absolute()

    def _deserialize(
            self,
            value: str,
            attr: Optional[str],
            data: Optional[Mapping[str, Any]],
            **kwargs
    ):
        deserialized = Path(value)
        if not deserialized.exists():
            raise ValidationError(f"field '{attr}' is not an existing path: '{value}'")
        return Path(value)


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


@mdataclass(frozen=True)
class MainConfig:
    music_path: Path = field(metadata={
        'marshmallow_field': MMPath(),
    })
    music_db_path: Path = field(metadata={
        'marshmallow_field': MMPath(),
    })
    static_playlists_path: Path = field(metadata={
        'marshmallow_field': MMPath(),
    })
    ice: IceConfig
    logging: LoggingConfig = LoggingConfig()
    default_query: str = ''
    bitrate: int = 4096
    Schema: ClassVar[Type[Schema]] = Schema


# Functions

def get_config(config_location: str):
    config_path = Path(config_location)
    with config_path.open() as file:
        raw_config = load(file, Loader=BaseLoader)
    main_config: MainConfig = MainConfig.Schema().load(raw_config)
    return main_config
