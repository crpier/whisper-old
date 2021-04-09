def main():
    """And app that whispers music to an IceCast server"""
    import uvicorn
    from fastapi import FastAPI, APIRouter
    from fastapi.middleware.cors import CORSMiddleware
    from starlette.staticfiles import StaticFiles

    from controllers.queue import radio_queue_router
    from controllers.station import station_router
    from setup import get_logger

    app = FastAPI()
    # TODO real cors
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )



    logger = get_logger()
    api_router = APIRouter()

    api_router.include_router(radio_queue_router, prefix="/queue")
    api_router.include_router(station_router, prefix="/station")

    app.include_router(api_router, prefix="/api")
    app.mount("/", StaticFiles(directory="src/static", html=True), name="static")

    logger.debug("Starting application")
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")


if __name__ == "__main__":
    main()
