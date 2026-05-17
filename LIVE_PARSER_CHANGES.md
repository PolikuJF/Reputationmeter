# Live parser fixes

Что изменено:

1. Кнопка «Запустить парсер» теперь пытается запускать существующий Selenium-парсер из `app/ParserReviews`.
2. Из ссылки Яндекс.Карт извлекается `org_id`.
3. Сгенерированный CSV сохраняется в `backend/app/ParserReviews/csv` внутри контейнера.
4. Затем `YandexCsvParser` читает свежий CSV и сохраняет отзывы в основную БД.
5. Исправлены импорты `backend.app...` на `app...` / относительные импорты.
6. В Dockerfile добавлен `firefox-esr`, чтобы Selenium мог запускаться внутри контейнера.

Важно:
- Live-парсинг Яндекс.Карт может занимать заметное время.
- Яндекс может менять верстку или блокировать Selenium, поэтому для production лучше подключить официальный API.
- Для полной пересборки backend используй:

```powershell
cd backend
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```
