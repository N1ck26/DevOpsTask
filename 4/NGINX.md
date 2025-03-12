### 4.1 Разобраться, как работают `proxy_pass`, `upstream`, `location`

#### `location`
Директива `location` в Nginx используется для определения того, как обрабатывать запросы к определенным URI. Она может быть настроена для обработки запросов на основе пути, регулярных выражений или других критериев.

Пример:
```nginx
location /app11 {
    # Обработка запросов к /app11
}
```

#### `proxy_pass`
Директива `proxy_pass` используется для перенаправления запросов на другой сервер. Она часто используется в связке с `location` для проксирования запросов на backend-серверы.

Пример:
```nginx
location /app11 {
    proxy_pass http://127.0.0.1:9999;
}
```

#### `upstream`
Директива `upstream` используется для определения группы серверов, на которые можно распределять запросы. Это полезно для балансировки нагрузки или резервирования.

Пример:
```nginx
upstream backend {
    server 127.0.0.1:9999;
    server 127.0.0.1:9998;
}

location /app11 {
    proxy_pass http://backend;
}
```

### 4.2 Настроить схему взаимодействия

#### User → FastAPI (для разработчика)
Для разработчика FastAPI может быть запущен локально, и запросы могут отправляться напрямую на FastAPI-сервер без использования Nginx.

Пример запуска FastAPI:
```bash
uvicorn main:app --host 127.0.0.1 --port 9999
```

#### User → Nginx → FastAPI (для DevOps)
Для DevOps-инфраструктуры Nginx выступает в роли прокси-сервера, который перенаправляет запросы на FastAPI.

Пример конфигурации Nginx:
```nginx
server {
    listen 80;
    server_name app11.devops;

    location /app11 {
        proxy_pass http://127.0.0.1:9999/app11;
    }
}
```

### 4.3 Привязать Nginx к домену

Чтобы привязать Nginx к домену `app11.devops` и перенаправлять запросы на `127.0.0.1:9999/app11`, нужно настроить конфигурацию Nginx следующим образом:

```nginx
server {
    listen 80;
    server_name app11.devops;

    location /app11 {
        proxy_pass http://127.0.0.1:9999/app11;
    }
}
```

### 4.4 Реализовать два варианта привязки

#### Вариант 1: `app1.devops/app11 → 127.0.0.1:9999/app11`
```nginx
server {
    listen 80;
    server_name app1.devops;

    location /app11 {
        proxy_pass http://127.0.0.1:9999/app11;
    }
}
```

#### Вариант 2: `app11.app1.devops → 127.0.0.1:9999/app11`
```nginx
server {
    listen 80;
    server_name app11.app1.devops;

    location / {
        proxy_pass http://127.0.0.1:9999/app11;
    }
}
```

### 4.5 Найти, где хранятся логи Nginx и в каком формате

Логи Nginx обычно хранятся в директории `/var/log/nginx/`. Основные логи:

- **access.log**: Логи всех запросов к серверу.
- **error.log**: Логи ошибок, возникающих при обработке запросов.

Формат логов можно настроить в конфигурации Nginx с помощью директивы `log_format`. По умолчанию используется комбинированный формат:

```nginx
log_format combined '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent"';
```

### 4.6 Изучить, что такое CORS и как он работает

**CORS (Cross-Origin Resource Sharing)** — это механизм, который позволяет веб-страницам делать запросы к другому домену, отличному от того, с которого была загружена страница. Это важно для безопасности, так как браузеры по умолчанию блокируют такие запросы (Same-Origin Policy).

#### Как работает CORS:
1. **Предварительный запрос (Preflight Request)**: Если запрос может повлиять на данные (например, POST, PUT, DELETE), браузер сначала отправляет запрос OPTIONS на сервер, чтобы узнать, разрешены ли такие запросы.
2. **Основной запрос**: Если сервер разрешает запрос, браузер отправляет основной запрос.

#### Настройка CORS в FastAPI:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все домены
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы
    allow_headers=["*"],  # Разрешить все заголовки
)
```

#### Настройка CORS в Nginx:
```nginx
add_header 'Access-Control-Allow-Origin' '*';
add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range';
```

Это основные моменты, которые помогут вам разобраться с поставленными задачами.