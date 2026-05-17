# Backend сервиса "Reputation Meter"

Backend-часть системы анализа отзывов. Реализует REST API для управления заведениями, отзывами, аутентификацией пользователей, анализом тональности и тематики отзывов, а также парсинг отзывов с Яндекс.Карт.

## Технологии

- **FastAPI** – веб-фреймворк
- **SQLAlchemy** – ORM
- **PostgreSQL** – база данных
- **Redis** – кеширование и брокер задач (опционально)
- **Selenium** – парсинг отзывов с Яндекс.Карт
- **Docker** – контейнеризация

## Структура проекта (бэкенд)
backend/
├── .dockerignore – исключения для Docker-образа
├── .env.example – пример переменных окружения
├── docker-compose.yml – оркестрация сервисов (postgres, redis, backend)
├── Dockerfile – инструкция сборки образа
├── requirements.txt – зависимости Python
├── README.md – этот файл
└── app/
├── init.py
├── alembic.ini – конфигурация миграций (опционально)
├── crud.py – CRUD операции с БД
├── database.py – настройка подключения к БД (синхронный SQLAlchemy)
├── main.py – точка входа FastAPI
├── models.py – SQLAlchemy модели
├── schemas.py – Pydantic схемы
├── email/ – отправка email-уведомлений
│ ├── init.py
│ └── sender.py
├── nlp/ – модуль анализа тональности и тем
│ ├── init.py
│ ├── mock_nlp.py – заглушка для тестов
│ ├── NLPSYSA.ipynb – ноутбук с реальной моделью
│ └── README.md – документация NLP-модуля
├── ParserReviews/ – парсер отзывов с Яндекс.Карт
│ ├── README.md
│ ├── requirements.txt
│ ├── run.py
│ ├── csv/ – примеры CSV с отзывами
│ └── parser/ – логика парсинга
├── routers/ – эндпоинты API
│ ├── init.py
│ ├── auth.py – регистрация, логин, JWT
│ ├── establishments.py – CRUD заведений
│ └── reviews.py – получение, обновление, анализ отзывов
└── tasks/ – фоновые задачи
├── init.py
└── analysis.py – асинхронный анализ отзыва

text

## Требования к компьютеру для запуска

- **Git**
- **Docker** и **Docker Compose** (рекомендуется)
- **Python 3.11+** (только для локальной разработки без Docker)
- **PostgreSQL** (если запускаете без Docker)

## Инструкция по запуску

### 1. Клонирование репозитория
```bash
git clone https://github.com/your-org/reputation-meter.git
cd reputation-meter/backend
2. Настройка переменных окружения
Скопируйте пример:

bash
cp .env.example .env
При необходимости отредактируйте параметры (база данных, SMTP, секретный ключ).

3. Запуск через Docker Compose (рекомендованный способ)
Из папки backend выполните:

bash
docker-compose up --build
Будут запущены:

PostgreSQL на порту 5432

Redis на порту 6379

Backend FastAPI на порту 8000

API будет доступно по адресу: http://localhost:8000
Документация Swagger: http://localhost:8000/docs

Чтобы остановить:

bash
docker-compose down
4. Запуск в режиме разработки (без Docker)
4.1 Установите PostgreSQL и Redis локально, либо используйте только PostgreSQL.
4.2 Создайте базу данных:
sql
CREATE DATABASE reputation_db;
4.3 Установите Python-зависимости:
bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
4.4 Настройте .env под ваше локальное окружение (DATABASE_URL, SECRET_KEY и т.д.)
4.5 Создайте таблицы в БД:
bash
python -c "from app.database import engine, Base; Base.metadata.create_all(bind=engine)"
4.6 Запустите сервер:
bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
5. Проверка работоспособности
Откройте http://localhost:8000/docs – должна открыться Swagger-документация.

Зарегистрируйте пользователя через POST /auth/register.

Получите JWT токен через POST /auth/login.

Добавьте заведение через POST /establishments.

Запустите парсинг отзывов (если интегрирован) или загрузите тестовые отзывы.

Просмотрите отзывы и дашборд через API.

Описание основных файлов и их назначение
Файл	Назначение
app/main.py	Инициализация FastAPI, подключение роутеров, создание таблиц БД
app/database.py	Настройка подключения к PostgreSQL (синхронный SQLAlchemy)
app/models.py	Описание таблиц: User, Establishment, Review, ParsingLog
app/crud.py	Функции для работы с БД (создание, чтение, обновление)
app/schemas.py	Pydantic-схемы для валидации входных/выходных данных
app/routers/auth.py	Регистрация, логин, выдача JWT
app/routers/establishments.py	CRUD для заведений, привязка к владельцу
app/routers/reviews.py	Получение отзывов, обновление статуса, запуск анализа
app/tasks/analysis.py	Фоновая обработка отзыва: сентимент, темы, email-уведомление при негативе
app/email/sender.py	Отправка уведомлений владельцу заведения о негативном отзыве
app/nlp/mock_nlp.py	Заглушка для анализа (всегда negative + фиксированные темы)
app/ParserReviews/	Модуль парсинга отзывов с Яндекс.Карт (Selenium)
docker-compose.yml	Определение сервисов: postgres, redis, backend
Dockerfile	Многостадийная сборка образа Python-приложения
.env.example	Пример переменных окружения
Возможные проблемы и решения
Ошибка подключения к БД
Убедитесь, что PostgreSQL запущен и DATABASE_URL корректен. В Docker-композе сервисы связаны по именам (postgres:5432).

Ошибка импорта модулей
Все директории (nlp, tasks, email, routers) должны содержать __init__.py. Они созданы в процессе настройки.

Нет таблиц в БД
При первом запуске таблицы создаются автоматически через Base.metadata.create_all(bind=engine) в main.py.

SMTP не настроен
Уведомления о негативных отзывах не будут отправляться, но работа системы не нарушится. В логах будет сообщение SMTP not configured.

Парсинг отзывов требует Firefox и geckodriver
В Docker-образе необходимо установить Firefox и geckodriver (не включено в текущий Dockerfile). Для MVP обычно используют заранее подготовленные CSV или mock-данные.

Дальнейшее развитие
Переход на асинхронный SQLAlchemy (asyncpg) для лучшей производительности.

Добавление миграций через Alembic.

Интеграция реальной NLP-модели (замена mock_nlp.py).

Использование Celery + Redis для фоновых задач вместо BackgroundTasks.

Разделение парсера в отдельный микросервис.