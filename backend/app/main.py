from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, establishments, reviews, dashboard, parsing
from app.tasks.scheduler import start_scheduler

app = FastAPI(title="Reputation Meter API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(establishments.router, prefix="/api/v1")
app.include_router(reviews.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")
app.include_router(parsing.router, prefix="/api/v1")

@app.on_event("startup")
def on_startup():
    start_scheduler()

@app.get("/")
async def root():
    return {"message": "Reputation Meter API"}
