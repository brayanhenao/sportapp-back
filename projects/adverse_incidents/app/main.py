import logging
from threading import Thread
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .components import notifier
from .exceptions.exceptions import NotFoundError

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting prioritizer thread")
    thread = Thread(target=notifier.get_incidents)
    thread.start()


@app.on_event("shutdown")
async def shutdown_event():
    notifier.stop_processing()


@app.exception_handler(NotFoundError)
async def not_found_error_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": str(exc)}
    )


@app.get("/ping")
async def root():
    return {"message": "Alerts Service"}
