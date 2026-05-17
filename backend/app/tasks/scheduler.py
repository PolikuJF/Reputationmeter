from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app import models
from app.database import SessionLocal
from app.services.parsing_service import run_parsing_for_establishment

scheduler = BackgroundScheduler(timezone="UTC")

def parse_all_active_establishments():
    db = SessionLocal()
    try:
        establishments = db.query(models.Establishment).filter(models.Establishment.is_archived == False).all()
        for establishment in establishments:
            try:
                run_parsing_for_establishment(db, establishment)
            except Exception:
                continue
    finally:
        db.close()

def start_scheduler():
    if scheduler.running:
        return
    scheduler.add_job(parse_all_active_establishments, CronTrigger(hour=3, minute=0), id="daily_reviews_parsing", replace_existing=True)
    scheduler.start()
