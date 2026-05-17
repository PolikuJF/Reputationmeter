from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, establishments, reviews, dashboard

# Отключаем автоматические редиректы с /path на /path/
app = FastAPI(title="Reputation Meter API", redirect_slashes=False)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создаём таблицы
Base.metadata.create_all(bind=engine)

# Подключаем роутеры с префиксом /api/v1
app.include_router(auth.router, prefix="/api/v1")
app.include_router(establishments.router, prefix="/api/v1")
app.include_router(reviews.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Reputation Meter API"}