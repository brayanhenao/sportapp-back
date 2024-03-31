from fastapi import FastAPI
from fastapi.responses import JSONResponse
from botocore.exceptions import ClientError
from .routes import users_routes
from .exceptions.exceptions import NotFoundError

app = FastAPI()

app.include_router(users_routes.router)


@app.exception_handler(NotFoundError)
async def not_found_error_handler(request, exc):
    return JSONResponse(status_code=404, content={"message": str(exc)})


@app.exception_handler(ClientError)
async def client_error_handler(request, exc):
    return JSONResponse(status_code=400, content={"message": exc.response["Error"]["Message"]})


@app.get("/ping")
async def root():
    return {"message": "Users Service"}
