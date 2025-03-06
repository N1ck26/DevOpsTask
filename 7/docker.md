Для выполнения задач 7.1, 7.2 и 7.3, следуйте пошаговым инструкциям ниже:

---

### 7.1 Обернуть backend-приложение в Docker-образ (создать Dockerfile, собрать образ)

1. **Создайте `Dockerfile`**:
   В корневой директории вашего backend-приложения создайте файл `Dockerfile` с содержимым:
   ```Dockerfile
   # Используем официальный образ Python
   FROM python:3.9-slim

   # Устанавливаем рабочую директорию
   WORKDIR /app

   # Копируем зависимости
   COPY requirements.txt .

   # Устанавливаем зависимости
   RUN pip install --no-cache-dir -r requirements.txt

   # Копируем исходный код приложения
   COPY . .

   # Указываем порт, который будет использовать приложение
   EXPOSE 8000

   # Команда для запуска приложения
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Соберите Docker-образ**:
   Выполните команду для сборки образа:
   ```bash
   docker build -t my-fastapi-app .
   ```

3. **Проверьте образ**:
   Убедитесь, что образ создан:
   ```bash
   docker images
   ```

---

### 7.2 Написать `docker-compose.yaml` для запуска nginx + postgres + FastAPI

1. **Создайте `docker-compose.yaml`**:
   В корневой директории проекта создайте файл `docker-compose.yaml` с содержимым:
   ```yaml
   version: '3.8'

   services:
     # Сервис для PostgreSQL
     db:
       image: postgres:13
       container_name: postgres_db
       environment:
         POSTGRES_USER: myuser
         POSTGRES_PASSWORD: mypassword
         POSTGRES_DB: mydatabase
       volumes:
         - postgres_data:/var/lib/postgresql/data
       ports:
         - "5432:5432"

     # Сервис для FastAPI
     backend:
       image: my-fastapi-app
       container_name: fastapi_app
       depends_on:
         - db
       environment:
         DATABASE_URL: postgresql://myuser:mypassword@db:5432/mydatabase
       ports:
         - "8000:8000"

     # Сервис для Nginx
     nginx:
       image: nginx:latest
       container_name: nginx_proxy
       depends_on:
         - backend
       ports:
         - "80:80"
       volumes:
         - ./nginx.conf:/etc/nginx/nginx.conf
       restart: always

   volumes:
     postgres_data:
   ```

2. **Создайте конфигурацию Nginx**:
   В той же директории создайте файл `nginx.conf`:
   ```nginx
   events {}

   http {
       server {
           listen 80;

           location / {
               proxy_pass http://backend:8000;
               proxy_set_header Host $host;
               proxy_set_header X-Real-IP $remote_addr;
               proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
               proxy_set_header X-Forwarded-Proto $scheme;
           }
       }
   }
   ```

3. **Запустите приложение**:
   Выполните команду:
   ```bash
   docker-compose up -d
   ```

4. **Проверка**:
   - FastAPI будет доступен по адресу `http://localhost:8000`.
   - Nginx будет проксировать запросы на FastAPI через `http://localhost`.

---

### 7.3 Обеспечить корректное подключение backend-а к базе (миграции можно выполнить вручную)

1. **Настройте подключение к базе данных**:
   Убедитесь, что в вашем FastAPI-приложении используется переменная окружения `DATABASE_URL` для подключения к PostgreSQL. Например:
   ```python
   from sqlalchemy import create_engine
   from sqlalchemy.ext.declarative import declarative_base
   from sqlalchemy.orm import sessionmaker

   DATABASE_URL = "postgresql://myuser:mypassword@db:5432/mydatabase"

   engine = create_engine(DATABASE_URL)
   SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   Base = declarative_base()
   ```

2. **Выполните миграции вручную**:
   Если вы используете Alembic для миграций, выполните следующие шаги:
   - Убедитесь, что Alembic настроен в вашем проекте.
   - Запустите контейнер с backend-приложением:
     ```bash
     docker exec -it fastapi_app /bin/bash
     ```
   - Внутри контейнера выполните команду для применения миграций:
     ```bash
     alembic upgrade head
     ```

3. **Проверка подключения**:
   - Убедитесь, что приложение корректно подключается к базе данных.
   - Проверьте, что таблицы созданы и данные могут быть записаны/прочитаны.

---

### Итог
- Backend-приложение обёрнуто в Docker-образ.
- Написан `docker-compose.yaml` для запуска Nginx, PostgreSQL и FastAPI.
- Обеспечено корректное подключение backend-а к базе данных.

Если возникнут вопросы, уточните, и я помогу!