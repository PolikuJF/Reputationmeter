# Review App – Система анализа отзывов

Веб-приложение для мониторинга и анализа отзывов о заведениях с автоматическим определением тональности (позитивные, нейтральные, негативные), выделением ключевых тем и управлением статусами отзывов.

## Технологии

- **Frontend**: React 18, TypeScript, Vite, Ant Design, TanStack Query, Axios, Recharts, React WordCloud.
- **Backend**  FastAPI / Django / другой .
- **Контейнеризация**: Docker, Nginx для раздачи статики.

## Структура проекта (клиентская часть)
frontend/
├── .dockerignore – исключения для Docker-образа
├── .env.example – пример переменных окружения
├── Dockerfile – инструкция сборки (многостадийная: build + nginx)
├── nginx.conf – конфигурация Nginx для SPA-маршрутизации
├── index.html – корневой HTML
├── package.json – зависимости и скрипты
├── vite.config.ts – конфигурация Vite (прокси, порт, плагин React)
├── tsconfig.json – конфигурация TypeScript (необходим для сборки)
├── tsconfig.node.json – конфиг для Node-среды (vite.config.ts)
└── src/
├── main.tsx – точка входа React
├── App.tsx – роутинг, проверка аутентификации, провайдеры
├── api/ – клиенты и вызовы API
│ ├── client.ts – инстанс axios с перехватчиком JWT
│ ├── dashboardApi.ts
│ ├── establishmentsApi.ts
│ └── reviewsApi.ts
├── components/ – переиспользуемые UI блоки
│ ├── common/
│ │ ├── Layout.tsx – основной лейаут (Sider + Header)
│ │ └── PtotectedRoute.tsx (опционально)
│ ├── dashboard/
│ │ ├── SentimentChart.tsx – график динамики тональности
│ │ └── TopicsCloud.tsx – облако тем
│ ├── establishments/
│ │ └── EstablishmentSelect.tsx
│ └── reviews/
│ ├── ReviewFilterBar.tsx
│ ├── ReviewStatusBadge.tsx
│ └── ReviewTable.tsx
├── hooks/ – кастомные хуки (React Query)
│ ├── useAuth.ts
│ ├── useDashboard.ts
│ ├── useEstablishments.ts
│ ├── useNotifications.ts
│ └── useReviews.ts
├── pages/ – страницы приложения
│ ├── DashboardPage.tsx
│ ├── EstablishmentsPage.tsx
│ └── LoginPage.tsx
└── types/ – TypeScript интерфейсы
└── index.ts

text

## Требования к компьютеру для запуска

- **Git** (чтобы клонировать репозиторий)
- **Node.js** v18+ и **npm** (только для разработки, при Docker не обязательны)
- **Docker** и **Docker Compose** (рекомендуется)
- **Backend API** – запущен отдельно на `http://localhost:8000` (или удалённый)

> Если вы хотите запустить **только фронтенд** в режиме разработки, потребуется Node.js. Для продакшн-подобного запуска используйте Docker.

## Инструкция по запуску

### 1. Клонирование репозитория
```bash
git clone https://github.com/your-org/review-app.git
cd review-app
2. Запуск бэкенда (обязательное условие)
Убедитесь, что бэкенд-сервер запущен и доступен по адресу http://localhost:8000.
Если бэкенд использует другой порт или хост, отредактируйте .env файл или переменные окружения.

3. Настройка переменных окружения (для разработки)
Скопируйте пример:

bash
cd frontend
cp .env.example .env
При необходимости измените VITE_API_URL на актуальный URL бэкенда.

4. Сборка и запуск через Docker (рекомендованный способ)
Из корня проекта выполните:

bash
cd frontend
docker build -t review-app-frontend .
docker run -d -p 8080:80 --name review-frontend review-app-frontend
Приложение будет доступно по адресу: http://localhost:8080

Чтобы остановить: docker stop review-frontend
Удалить контейнер: docker rm review-frontend

5. Запуск в режиме разработки (без Docker)
bash
cd frontend
npm install
npm run dev
Сервер разработки Vite запустится на http://localhost:3000.
Прокси автоматически перенаправит запросы /api на http://localhost:8000/api/v1.

6. Проверка работоспособности
Откройте http://localhost:8080 (или http://localhost:3000).

Войдите в систему: любой логин/пароль (демо-режим, токен сохраняется в localStorage).

После входа откроется дашборд с графиком тональности, облаком тем и списком отзывов.

Перейдите в раздел "Заведения", чтобы добавить или архивировать источники отзывов.

Описание основных файлов и их назначение
Файл	Назначение
src/App.tsx	Маршрутизация, проверка аутентификации, обёртка QueryClientProvider
src/api/client.ts	Настройка axios с baseURL и перехватчиком для JWT
src/api/dashboardApi.ts	Функции для получения сводных данных (обзор, тренды)
src/components/dashboard/SentimentChart.tsx	График динамики тональности (LineChart из recharts) с фильтрацией
src/components/dashboard/TopicsCloud.tsx	Облако самых частотных тем (react-wordcloud)
src/components/reviews/ReviewTable.tsx	Таблица отзывов с возможностью изменения статуса, пагинация
src/hooks/useReviews.ts	Хуки для получения списка отзывов и обновления статуса (React Query)
src/hooks/useDashboard.ts	Хук для получения данных дашборда с кешированием
src/pages/EstablishmentsPage.tsx	Управление заведениями: добавление по URL, архивация
Dockerfile	Многостадийная сборка: npm run build + Nginx, экспорт порта 80
nginx.conf	Настройка Nginx: корень /usr/share/nginx/html, fallback на index.html для SPA
vite.config.ts	Плагин React, dev-сервер с прокси на бэкенд, папка сборки dist
Возможные проблемы и решения
Ошибка соединения с API
Проверьте, что бэкенд запущен и VITE_API_URL указывает верный адрес. При Docker-запуске бэкенд должен быть доступен с хоста (например, http://host.docker.internal:8000).

Пустая страница или 404 при обновлении
Убедитесь, что Nginx настроен с try_files $uri $uri/ /index.html. Наш nginx.conf это учитывает.

Не импортируется ShopOutlined
Файл Layout.tsx уже исправлен – импорт добавлен.

Отсутствуют типы TypeScript
В package.json есть все необходимые @types/*. При локальной разработке выполните npm install.

Дальнейшее развитие
Подключение реальной аутентификации через JWT (сейчас демо-заглушка).

WebSocket уведомления о новых негативных отзывах (в useNotifications уже есть polling).

Добавление пагинации на дашборде для таблицы отзывов.

Расширенная фильтрация по датам, источникам.