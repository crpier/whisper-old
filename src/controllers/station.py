import json

from broadcaster import Broadcast, Event
from fastapi import APIRouter, Depends, WebSocket

from services.station import StreamMetadata, StationContainer
from setup import get_library, get_station_container, get_logger
import logging
import websockets

station_router = APIRouter()


@station_router.websocket("/status")
async def get_station_status(
    ws: WebSocket,
    station_container: StationContainer = Depends(get_station_container),
    logger=Depends(get_logger),
):
    try:
        container_status = station_container.get_container_status()
        await ws.accept()
        if container_status != {}:
            await ws.send_json(container_status)
        logger.debug("Socket opened")
        broadcast = Broadcast("redis://localhost:6379")
        await broadcast.connect()
        async with broadcast.subscribe("song_change") as subscriber:
            change: Event
            async for change in subscriber:
                container_status = station_container.get_container_status()
                logger.debug(f"Container status: {container_status}")
                await ws.send_json(json.dumps(container_status))
    except websockets.exceptions.ConnectionClosedOK:
        logger.debug("Socket closed unexpectedly")


# TODO make autostart depend on env or config
# @station_router.on_event('startup')
@station_router.post("/")
def create_station(
    query: str = "aa",
    name: str = "lol",
    mount: str = "/lol",
    genre: str = "kek",
    description: str = "stuff",
    station_container: StationContainer = Depends(get_station_container),
):
    metadata = StreamMetadata(name, mount, genre, description)
    new_station = station_container.create_station(metadata)
    library = get_library()
    items = library.items(query)
    # logger.debug("populating queue for station {}".format(name))
    for item in items:
        new_station.radio_queue.add_to_queue(item)
    new_station.start_radio()
    return {"status": "SUCCESS", "data": new_station.metadata}


@station_router.delete("/")
async def remove_radio(
    name: str, station_container: StationContainer = Depends(get_station_container)
):
    await station_container.remove_station(name)
    return {
        "status": "SUCCESS",
    }


@station_router.patch("/pause")
def pause_radio(
    name: str, station_container: StationContainer = Depends(get_station_container)
):
    station = station_container.get_station(name)
    station.pause_playing()
    return {"status": "SUCCESS"}


@station_router.patch("/unpause")
def unpause_radio(
    name: str, station_container: StationContainer = Depends(get_station_container)
):
    station = station_container.get_station(name)
    station.unpause_playing()
    return {"status": "SUCCESS"}


@station_router.patch("/skip")
def skip_song(
    name: str, station_container: StationContainer = Depends(get_station_container)
):
    station = station_container.get_station(name)
    station.skip_song()
    return {"status": "SUCCESS"}
