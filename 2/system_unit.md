### 2.1 Написание Python-приложения (Flask/FastAPI) и запуск двух экземпляров

Для начала создадим простое Flask-приложение, которое будет отдавать веб-страницы на разных портах.

1. Установим Flask, если он еще не установлен:

   ```bash
   pip install flask
   ```

2. Создадим файл `app.py` с следующим содержимым:

   ```python
   from flask import Flask

   app = Flask(__name__)

   @app.route('/app11')
   def app11():
       return 'Hello from app11!'

   @app.route('/app12')
   def app12():
       return 'Hello from app12!'

   @app.route('/app21')
   def app21():
       return 'Hello from app21!'

   @app.route('/app22')
   def app22():
       return 'Hello from app22!'

   if __name__ == '__main__':
       app.run(port=9999)  # Первый экземпляр на порту 9999
   ```

3. Запустим два экземпляра приложения на разных портах:

   - Первый экземпляр на порту 9999:

     ```bash
     python app.py
     ```

   - Второй экземпляр на порту 9998:

     ```bash
     FLASK_APP=app.py flask run --port=9998
     ```

Теперь приложение будет доступно по адресам:

- `http://127.0.0.1:9999/app11`
- `http://127.0.0.1:9999/app12`
- `http://127.0.0.1:9998/app21`
- `http://127.0.0.1:9998/app22`

### 2.2 Написание systemd-юнита для приложения

Создадим systemd-юнит для управления нашим приложением.

1. Создадим файл юнита `/etc/systemd/system/myapp.service`:

   ```ini
   [Unit]
   Description=My Flask Application
   After=network.target

   [Service]
   User=app
   WorkingDirectory=/path/to/your/app
   ExecStart=/usr/bin/python3 /path/to/your/app/app.py
   ExecStart=/usr/bin/flask run --port=9998
   Restart=always
   StandardOutput=append:/var/log/myapp.log
   StandardError=append:/var/log/myapp.error.log

   [Install]
   WantedBy=multi-user.target
   ```

   Замените `/path/to/your/app` на путь к вашему приложению.

2. Перезагрузим systemd, чтобы применить изменения:

   ```bash
   sudo systemctl daemon-reload
   ```

3. Теперь можно управлять приложением с помощью команд:

   - Запуск:

     ```bash
     sudo systemctl start myapp
     ```

   - Остановка:

     ```bash
     sudo systemctl stop myapp
     ```

   - Проверка статуса:

     ```bash
     sudo systemctl status myapp
     ```

### 2.3 Настройка запуска systemd-юнита от пользователя `app`

1. Создадим пользователя `app`, если он еще не существует:

   ```bash
   sudo adduser app
   ```

2. Убедимся, что пользователь `app` имеет доступ к директории с приложением:

   ```bash
   sudo chown -R app:app /path/to/your/app
   ```

3. В файле юнита `/etc/systemd/system/myapp.service` уже указан пользователь `app` в секции `[Service]`.

### 2.4 Обеспечение автозапуска юнита после перезагрузки системы

1. Включим автозапуск юнита:

   ```bash
   sudo systemctl enable myapp
   ```

2. Проверим, что юнит добавлен в автозагрузку:

   ```bash
   sudo systemctl is-enabled myapp
   ```

Теперь ваше приложение будет автоматически запускаться после перезагрузки системы.