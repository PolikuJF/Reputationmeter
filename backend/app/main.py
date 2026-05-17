from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, establishments, reviews

app = FastAPI(title="Reputation Meter API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создаём таблицы при старте (синхронно)
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(establishments.router)
app.include_router(reviews.router)

@app.get("/")
async def root():
    return {"message": "Reputation Meter API"}