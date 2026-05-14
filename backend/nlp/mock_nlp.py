import random

def analyze_sentiment(text: str) -> str:
    # Заглушка – для теста всегда negative или случайно
    # Позже заменим на реальную модель
    return "negative"  # или random.choice(["positive", "neutral", "negative"])

def extract_topics(text: str) -> list:
    # Заглушка: возвращает фиксированный список тем
    return ["обслуживание", "качество еды"]