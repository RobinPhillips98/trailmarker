"""Initializes and launches the server itself."""

import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models
from api.routes import auth, characters, encounters, enemies, simulation, user
from db import engine

is_production = os.getenv("ENVIRONMENT") == "production"

app = FastAPI(
    docs_url=None if is_production else "/docs",
    redoc_url=None if is_production else "/redoc",
    debug=not is_production
)

origins = [
    "http://localhost:5173",
    "https://trailmarker2e.com",
    "https://www.trailmarker2e.com",
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
app.include_router(user.router)
app.include_router(auth.router, prefix="/auth")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
