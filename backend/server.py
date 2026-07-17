"""Initializes and launches the server itself."""

import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models
from api.routes import auth, characters, encounters, enemies, simulation, users
from db import engine

is_production = os.getenv("ENVIRONMENT") == "production"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI application.

    This function is called when the FastAPI application starts and stops. It
    creates the database tables defined in the models if they do not already
    exist when the application starts.

    """
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield


app = FastAPI(
    lifespan=lifespan,
    docs_url=None if is_production else "/docs",
    redoc_url=None if is_production else "/redoc",
    debug=not is_production,
)

origins = [
    "http://localhost:5173",  # Local dev server
    "http://localhost:8080",  # Local production test server
    "https://trailmarker2e.com",
    "https://www.trailmarker2e.com",
    os.getenv("FRONTEND_URL"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(characters.router)
app.include_router(enemies.router)
app.include_router(encounters.router)
app.include_router(simulation.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Server is running!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
