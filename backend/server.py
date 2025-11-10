import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models
from api.routes import enemies, encounters
from db import engine

app = FastAPI(debug=True)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(enemies.router)
app.include_router(encounters.router)

models.Base.metadata.create_all(bind=engine)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# db = Annotated[Session, Depends(get_db)]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
