POSITIVE_WORDS = ["отлично", "вкусно", "хорошо", "понравилось", "супер", "классно", "быстро", "приятно", "рекомендую", "люблю"]
NEGATIVE_WORDS = ["плохо", "ужасно", "отвратительно", "долго", "хамство", "грязно", "невкусно", "дорого", "разочарован", "кошмар"]

def analyze_sentiment(text: str) -> str:
    text = (text or "").lower()
    positive_score = sum(word in text for word in POSITIVE_WORDS)
    negative_score = sum(word in text for word in NEGATIVE_WORDS)
    if positive_score > negative_score:
        return "positive"
    if negative_score > positive_score:
        return "negative"
    return "neutral"

def extract_topics(text: str) -> list[str]:
    text = (text or "").lower()
    topics = []
    if any(word in text for word in ["официант", "персонал", "обслуживание", "сервис"]): topics.append("обслуживание")
    if any(word in text for word in ["еда", "ролл", "суши", "вкус", "блюдо"]): topics.append("еда")
    if any(word in text for word in ["долго", "быстро", "ожидание", "доставка"]): topics.append("скорость")
    if any(word in text for word in ["цена", "дорого", "дешево", "стоимость"]): topics.append("цены")
    return topics or ["общее"]
