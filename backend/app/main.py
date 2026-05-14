from fastapi import FastAPI, Depends
from app.database import engine, Base, get_db
from app.routers import auth, establishments, reviews

app = FastAPI(title="Reputation Meter API")

@app.on_event("startup")
def init_db():
    Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(establishments.router)
app.include_router(reviews.router)

@app.get("/")
async def root():
    return {"message": "Reputation Meter API"}