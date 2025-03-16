1. Пишем приложение которое отдает веб-страницы на разных портах:
   ```
   127.0.0.1:9999/app11, 127.0.0.1:9999/app12
   127.0.0.1:9998/app21, 127.0.0.1:9998/app22
   ```

2. Создаем пользователя app `sudo useradd -m -s /bin/bash app`

3. Пишем system-unit:
   ```
   User=app #пользователь 

   Group=app #группа

   WorkingDirectory=/home/app/FastAPI_app #определяем рабочую директорию

   ExecStart=/home/app/FastAPI_app/venv/bin/python3 /home/app/FastAPI_app/app.py #выполнение команды для запуска приложения

   Restart=always #приложение будет перезапускаться в любых случаях 

   RestartSec=5 #задержка в 5 секунд перед перезапуском сервиса после его завершения с ошибкой.

   StandardOutput=append:/var/log/devops-app.log #все логи с приложения будут добавляться в файл `var/log/devops-app.log`

   StandardError=append:/var/log/devops-app.error.log #все логи ошибок будут добавляться в файл `var/log/devops-app.error.log`
   ```

4. Создаем файлы для логов и предоставляем пользователю app доступ к ним
   ```
   sudo touch /var/log/devops-app.log /var/log/devops-app.error.log

   sudo chown app:app /var/log/devops-app.log /var/log/devops-app.error.log
   ```

5. Перезапускаем `systemd`: `sudo systemctl daemon-reload`

6. Перезапускаем сам сервис: `sudo systemctl restart devops-app.service`

7. Проверяем его статус: `sudo systemctl status devops-app.service`

8. Добавляем юнит в автозапуск: `sudo systemctl enable devops-app.service` 

9. Дальше можно использровать команды для остановки и запуска юнита:
   ```
   sudo systemctl stop devops-app.service
   sudo systemctl start devops-app.service
   ```