import os
import sys

from fastapi import FastAPI

from .routes import provider

app = FastAPI()

app.include_router(provider.router)


@app.on_event("startup")
async def verify_api_key_set():
    if not os.getenv("API_KEY"):
        print("API_KEY not set")
        sys.exit("API_KEY not set")


@app.get("/ping")
async def root():
    return {"message": "Adverse Incidents Provider"}
