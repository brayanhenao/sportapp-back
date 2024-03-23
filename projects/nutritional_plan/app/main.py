from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .routes import nutritional_plan
from .exceptions.exceptions import NotFoundError

app = FastAPI()

app.include_router(nutritional_plan.router)


@app.exception_handler(NotFoundError)
async def not_found_error_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": str(exc)}
    )


@app.get("/ping")
async def root():
    return {"message": "Nutritional Plan Service"}
