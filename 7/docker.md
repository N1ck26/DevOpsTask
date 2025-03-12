1. Создаем Dockerfile:
    1.1. Пулим образ python: `FROM python:3.10`
    1.2. Устанавливаем рабочию директорию: `WORKDIR /app`
    1.3. Копируем все локальные файлы в контейнер: `COPY . .`
    1.4. Установка зависимостей для работы с приложением: `RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy psycopg2-binary`
    1.5. Открываем порт: `EXPOSE 8000`
    1.6. Запускаем сервер: `CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]`