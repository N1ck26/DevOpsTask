1. <i>Dockerfile:</i>

    1.1. Пулим образ python: `FROM python:3.10`

    1.2. Устанавливаем рабочию директорию: `WORKDIR /app`

    1.3. Копируем все локальные файлы в контейнер: `COPY . .`

    1.4. Установка зависимостей для работы с приложением: `RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy psycopg2-binary`

    1.5. Открываем порт: `EXPOSE 8000`

    1.6. Запускаем сервер: `CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]`

2. <i>nginx.conf:</i>

    2.1. Для дальнейшей возможной масштабируемости сервиса с помощью `upstream` определяю группу серверов (в данном случае один сервер) на которых будет распределяться нагрузка

    2.2. Определяю с помощью `server backend:8000` адрес и порт сервера, где `backend` использую в качестве имени сервера (название идет из docker-compose.yml) 

    2.3. В блоке server указываю, чтобы nginx слушал 80 порт `listen 80`

    2.4. `proxy_pass http://backend;` проксируем все запросы на указанные с помощью `upstream` сервера (в моем случае он один)

    2.5. `proxy_set_header` Устанавливаем заголовки для передачи дополнительной информации на backend

    2.6. `Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`,`Access-Control-Allow-Headers` - CORS-заголовки

3. <i>docker-compose.yml:</i>

    3.1. Postgres:
    -
    ```
    db: # название сервиса
      image: postgres:15 # указываем образ
      container_name: postgres_container # задаем название контейнеру
      restart: always # постоянный перезапуск сервиса после его завершения работы
      environment: # определяем параметры переменного окружения
        POSTGRES_USER: postgres
        POSTGRES_PASSWORD: password
        POSTGRES_DB: test_db
      ports: # прокидываем сетевые порты( порт хоста : порт контейнера )
        - "5432:5432"
      volumes: # монтируем данные между хост-машиной и контейнером
        - postgres_data:/var/lib/postgresql/data 
    ```

    3.2. Backend
    -
    ```
    backend: # название сервиса
      build: . # указываем что в текущей директории есть dockerfilе, который необходимо собрать
      container_name: fastapi_container # задаем название контейнеру
      restart: always # постоянный перезапуск сервиса после его завершения работы
        depends_on: # определяет очередность запуска контейнеров (запускает backend после базы данных)
        - db
      environment: # определяем параметры переменного окружения
        DATABASE_URL: postgresql://postgres:password@db/test_db # переменная которая использвуется для подключения к бд
      ports: # прокидываем сетевые порты( порт хоста : порт контейнера )
      - "8000:8000"
    ```

    3.3. Nginx
    -
    ```
    nginx:  # название сервиса
      image: nginx:latest # указываем образ (lastes значит самый последний)
      container_name: nginx_container # задаем название контейнеру
      restart: always# постоянный перезапуск сервиса после его завершения работы
      ports: # прокидываем сетевые порты( порт хоста : порт контейнера )
        - "80:80"
      volumes: # монтируем данные между хост-машиной и контейнером
        - ./nginx.conf:/etc/nginx/nginx.conf:ro
      depends_on: определяет очередность запуска контейнеров (запускает nginx после backend)
        - backend
    ```

4. Теперь можно поднять всё одной командой `docker-compose up -d`
        
