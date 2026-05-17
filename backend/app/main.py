from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
<<<<<<< HEAD
from app.routers import auth, establishments, reviews, dashboard, parsing
from app.tasks.scheduler import start_scheduler

app = FastAPI(title="Reputation Meter API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:3000", "http://localhost:5173"],
=======
from app.routers import auth, establishments, reviews, dashboard

# Отключаем автоматические редиректы с /path на /path/

app = FastAPI(title="Reputation Meter API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:3000"],
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

<<<<<<< HEAD
Base.metadata.create_all(bind=engine)

=======
# Создаём таблицы
Base.metadata.create_all(bind=engine)

# Подключаем роутеры с префиксом /api/v1
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
app.include_router(auth.router, prefix="/api/v1")
app.include_router(establishments.router, prefix="/api/v1")
app.include_router(reviews.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")
<<<<<<< HEAD
app.include_router(parsing.router, prefix="/api/v1")

@app.on_event("startup")
def on_startup():
    start_scheduler()

@app.get("/")
async def root():
    return {"message": "Reputation Meter API"}
=======

@app.get("/")
async def root():
    return {"message": "Reputation Meter API"}
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
