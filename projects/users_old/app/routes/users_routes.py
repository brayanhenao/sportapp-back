from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse

from ..models.schemas.schema import UserCreate, UserCredentials
from ..services.users_service import UsersService

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def register_user(user: UserCreate, users_service: UsersService = Depends()):
    user_created_response = users_service.register_user(user)
    return JSONResponse(content=user_created_response, status_code=201)


@router.patch("/{user_id}/complete-registration")
async def complete_user_registration(user_id: str, users_service: UsersService = Depends()):
    user_created_response = users_service.complete_user_registration(user_id)
    return JSONResponse(content=user_created_response, status_code=200)


@router.get("/{user_id}")
async def get_user(user_id: str, users_service: UsersService = Depends()):
    user = users_service.get_user(user_id)
    return JSONResponse(content=user, status_code=200)


@router.delete("/{user_id}")
async def delete_user(user_id: str, users_service: UsersService = Depends()):
    user = users_service.delete_user(user_id)
    return JSONResponse(content=user, status_code=200)


@router.get("/")
async def get_users(users_service: UsersService = Depends()):
    users = users_service.get_users()
    return JSONResponse(content=users, status_code=200)


@router.post("/login")
async def login_user(user_credentials: UserCredentials, users_service: UsersService = Depends()):
    auth = users_service.login_user(user_credentials)
    return JSONResponse(content=auth, status_code=200)
