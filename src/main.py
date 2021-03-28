import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from controllers.queue import radio_queue_router
from controllers.station import station_router
from setup import logger

app = FastAPI()
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(radio_queue_router, prefix='/queue')
app.include_router(station_router, prefix='/station')
app.mount('/client',
          StaticFiles(directory='src/static', html=True),
          name='static')


async def sync_shout(shout_connection):
    shout_connection.sync()


logger.debug('Starting application')
uvicorn.run(app, host='0.0.0.0', port=8001, log_level='info')
