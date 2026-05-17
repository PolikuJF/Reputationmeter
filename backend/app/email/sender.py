import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)

def send_negative_review_notification(owner_email: str, establishment_name: str, review_text: str):
    if not SMTP_USER or not SMTP_PASSWORD:
        print("SMTP not configured – email not sent")
        return
    
    msg = EmailMessage()
    msg["Subject"] = f"⚠️ Новый негативный отзыв в {establishment_name}"
    msg["From"] = FROM_EMAIL
    msg["To"] = owner_email
    msg.set_content(f"""
Здравствуйте!

Получен новый негативный отзыв на ваше заведение "{establishment_name}":

"{review_text[:500]}"

Пожалуйста, зайдите в дашборд для ответа.

С уважением,
Reputation Meter
""")
    
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)