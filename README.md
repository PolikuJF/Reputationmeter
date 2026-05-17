# Reputationmeter

## Запуск бэкенда (в терминале 1)

cd backend

docker-compose up --build

## Запуск фронтенда (в терминале 2)

cd frontend

docker build -t review-app-frontend .

docker run -d -p 8080:80 --name review-frontend review-app-frontend


Сайт доступен по ссылке:  

http://localhost:8080

## Остановка контейнеров

**Бэкенд:** в первом терминале нажмите `Ctrl+C`, затем: docker-compose down

**Фронтенд:** docker stop review-frontend && docker rm review-frontend
