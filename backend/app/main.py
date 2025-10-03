from fastapi import Depends, FastAPI
from app.routers import get_calories, auth

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis
from contextlib import asynccontextmanager
from app.config import Settings

@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_connection = redis.from_url(Settings().redis_url, encoding="utf8")
    await FastAPILimiter.init(redis_connection)
    yield
    await FastAPILimiter.close()

app = FastAPI(lifespan=lifespan)

@app.get("/", dependencies=[Depends(RateLimiter(times=15, seconds=60))])
async def root():
    return {"message": "Welcome to the Meal Calorie API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


app.include_router(get_calories.router)
app.include_router(auth.router)
