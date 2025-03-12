1. Кодим приложуху
2. Пишем system-unit для него:
   ```
   [Unit]
   Description=FastAPI app for DevOps Task
   After=network.target

   [Service]
   User=app
   Group=app
   WorkingDirectory=/home/app/DevOpsTask/2/FastAPI
   ExecStart=/home/app/DevOpsTask/2/FastAPI/venv/bin/python3 /home/app/DevOpsTask/2/FastAPI/app.py
   Restart=always
   RestartSec=5
   StandardOutput=append:/var/log/devops-app.log
   StandardError=append:/var/log/devops-app.error.log

   [Install]
   WantedBy=multi-user.target
   ```
3. 