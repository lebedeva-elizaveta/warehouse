from fastapi import FastAPI, Request
from app.views import router as roll_router

app = FastAPI()

app.include_router(roll_router)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = await call_next(request)
    return response
