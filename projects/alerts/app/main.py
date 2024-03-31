import logging
from threading import Thread
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .components import prioritizer
from .routes import alerts
from .exceptions.exceptions import NotFoundError

app = FastAPI()

app.include_router(alerts.router)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting prioritizer thread")
    thread = Thread(target=prioritizer.process_queues)
    thread.start()


@app.on_event("shutdown")
async def shutdown_event():
    prioritizer.stop_processing()


@app.exception_handler(NotFoundError)
async def not_found_error_handler(request, exc):
    return JSONResponse(status_code=404, content={"message": str(exc)})


@app.get("/ping")
async def root():
    return {"message": "Alerts Service"}
