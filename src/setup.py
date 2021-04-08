import logging
import sys
from functools import lru_cache
from beets.library import Library

from config import Settings
from services.station import StationContainer


@lru_cache(maxsize=1)
def get_logger():
    config = get_config()
    app_logger = logging.getLogger(__name__)
    handler = logging.FileHandler(config.log_file)
    stoud_handler = logging.StreamHandler(sys.stdout)
    app_format = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
    handler.setFormatter(app_format)
    stoud_handler.setFormatter(app_format)
    app_logger.addHandler(handler)
    app_logger.addHandler(stoud_handler)
    app_logger.level = config.log_level
    return app_logger


@lru_cache(maxsize=1)
def get_station_container():
    config = get_config()
    logger = get_logger()

    return StationContainer(config.stream_bitrate, logger, config.ice_host,
                            config.ice_password, config.ice_user,
                            config.ice_port, config.ice_format)


@lru_cache(maxsize=1)
def get_config():
    return Settings()


@lru_cache(maxsize=1)
def get_library():
    config = get_config()
    return Library(bytes(config.beets_music_db_path))
