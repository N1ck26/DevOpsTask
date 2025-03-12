1. Создаем Dockerfile:
    1.1. Пулим образ python: `FROM python:3.10`
    1.2. Устанавливаем рабочию директорию: `WORKDIR /app`
    1.3. Копируем все локальные файлы в контейнер: `COPY . .`
    1.4. Установка зависимостей для работы с приложением: `RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy psycopg2-binary`
    1.5. Открываем порт: `EXPOSE 8000`
    1.6. Запускаем сервер: `CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]`

2. Конфиг nginx:
    2.1. Для дальнейшей масштабируемости сервиса с помощью `upstream` определяю группу серверов (в данном случае один сервер)
    2.2. Определяю с помощью `server backend:8000` адрес и порт сервера, где `backend` использую в качестве имени сервера (название идет из docker-compose.yml) 
    2.3. В блоке server указываю, чтобы nginx слушал 80 порт `listen 80`
    2.4. `proxy_pass http://backend;` проксируем все запросы на указанный с помощью `upstream` сервера (в моем случае он один)
    2.5. `proxy_set_header` Устанавливаем заголовки для передачи дополнительной информации на backend
    2.6. `Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`,`Access-Control-Allow-Headers` - CORS-заголовки 