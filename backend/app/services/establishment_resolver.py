from urllib.parse import urlparse
from fastapi import HTTPException

async def resolve_establishment_by_url(url: str) -> dict:
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise HTTPException(status_code=400, detail="Некорректная ссылка")
    host = parsed.netloc.lower()
    if "yandex" in host:
        platform_type = "yandex"
    elif "google" in host or "goo.gl" in host:
        platform_type = "google"
    elif "2gis" in host:
        platform_type = "2gis"
    else:
        raise HTTPException(status_code=400, detail="Поддерживаются ссылки Яндекс.Карт, Google Maps или 2ГИС")
    return {"name": "Заведение", "address": None, "platform_url": url, "platform_type": platform_type, "external_id": url}
