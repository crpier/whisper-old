import logging
import os
import sys
from functools import lru_cache

from beets.library import Library

from config import get_config, LoggingConfig, MainConfig
from services.station import StationContainer


def get_logger(logging_config: LoggingConfig):
    app_logger = logging.getLogger(__name__)
    handler = logging.FileHandler(logging_config.filename)
    stoud_handler = logging.StreamHandler(sys.stdout)
    app_format = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
    handler.setFormatter(app_format)
    stoud_handler.setFormatter(app_format)
    app_logger.addHandler(handler)
    app_logger.addHandler(stoud_handler)
    app_logger.level = logging_config.level
    return app_logger


@lru_cache()
def get_station_container():
    return StationContainer(config.ice, config.bitrate, logger)


config: MainConfig = get_config(os.getenv('CONFIG_LOCATION'))
logger = get_logger(config.logging)
library = Library(str(config.music_db_path))
