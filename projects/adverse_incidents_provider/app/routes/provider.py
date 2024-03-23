import os
from typing import Annotated

from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import JSONResponse

from ..services.provider import randomize_adverse_incidents

router = APIRouter(
    prefix="/incidents",
    tags=["incidents"],
    responses={404: {"description": "Not found"}},
)


def validate_api_key(x_api_key: str = Header(None)):
    if x_api_key is None:
        raise HTTPException(status_code=401, detail="x-api-key header is missing")
    if x_api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key


@router.get("/")
async def generate_adverse_incidents(x_api_key: Annotated[str | None, Header()] = None):
    validate_api_key(x_api_key)
    incidents = randomize_adverse_incidents()
    return JSONResponse(status_code=200, content={
        "incidents": [incident.to_dict() for incident in incidents]
    })
