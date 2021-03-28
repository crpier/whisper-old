from fastapi import APIRouter, Depends

from services.station import StationContainer, RadioQueue
from setup import get_library, get_station_container

radio_queue_router = APIRouter()
library = get_library()


@radio_queue_router.get("/")
def get_radio_queue(
    name: str,
    page_size: int = 20,
    page_number: int = 1,
    station_container: StationContainer = Depends(get_station_container)):
    all_songs = station_container. \
            get_station(name). \
            radio_queue. \
            get_serialized_queue()
    if page_size > 0:
        songs = all_songs[page_size * (page_number - 1):page_size *
                          page_number]
        last_page = len(all_songs) // page_size + 1
    else:
        songs = all_songs
        last_page = 1
    return {
        "status": "SUCCESS",
        "page_number": page_number,
        "page_size": page_size,
        "last_page": last_page,
        "data": songs
    }


# TODO websocket should be used for cheap instant whatever
@radio_queue_router.get('/current')
def get_current_song(
    name: str,
    station_container: StationContainer = Depends(get_station_container)):
    radio_queue: RadioQueue = station_container.get_station(name).radio_queue
    current_song = radio_queue.get_current_song()
    return {"status": "SUCCESS", "data": current_song}


@radio_queue_router.put("/")
def add_to_queue(
    name: str,
    query: str = "",
    station_container: StationContainer = Depends(get_station_container)):
    radio_queue: RadioQueue = station_container.get_station(name).radio_queue
    items = library.items(query)
    for item in items:
        radio_queue.add_to_queue(item)
    return {"status": "SUCCESS"}


@radio_queue_router.delete("/")
def clear_queue(
    name: str,
    station_container: StationContainer = Depends(get_station_container)):
    radio_queue: RadioQueue = station_container.get_station(name).radio_queue
    radio_queue.clear_radio_queue()
    return {"status": "SUCCESS"}
