from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse

from ..models.schemas.schema import SportSessionStart, SportSessionLocationUpdate
from ..services.sport_session import SportSessionService

router = APIRouter(
    prefix="/sport-session",
    tags=["sport-session"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def start_sport_session(sport_session: SportSessionStart,
                              sport_session_service: SportSessionService = Depends()):
    sport_session = sport_session_service.start_sport_session(sport_session)
    return JSONResponse(content=sport_session, status_code=201)


@router.patch("/{sport_session_id}/finish")
async def finish_sport_session(sport_session_id: str, calories: float,
                               sport_session_service: SportSessionService = Depends()):
    sport_session = sport_session_service.finish_sport_session(sport_session_id, calories)
    return JSONResponse(content=sport_session, status_code=200)


@router.patch("/{sport_session_id}/location")
async def update_sport_session_location(sport_session_id: str, location: SportSessionLocationUpdate,
                                        sport_session_service: SportSessionService = Depends()):
    sport_session = sport_session_service.update_sport_session_location(sport_session_id, location)
    return JSONResponse(content=sport_session, status_code=200)


@router.get("/active-sessions")
async def get_active_sport_sessions(sport_session_service: SportSessionService = Depends()):
    sport_sessions = sport_session_service.get_active_users_locations()
    return JSONResponse(content=sport_sessions, status_code=200)


@router.get("/")
async def get_all_sessions(sport_session_service: SportSessionService = Depends()):
    sport_sessions = sport_session_service.get_sport_sessions()
    return JSONResponse(content=sport_sessions, status_code=200)
