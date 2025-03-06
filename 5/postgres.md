### 5.1 Установить PostgreSQL в single-node режиме

1. **Установка PostgreSQL**:
   - На Ubuntu/Debian:
     ```bash
     sudo apt update
     sudo apt install postgresql postgresql-contrib
     ```
   - На CentOS/RHEL:
     ```bash
     sudo yum install postgresql-server postgresql-contrib
     sudo postgresql-setup initdb
     ```

2. **Запуск и включение в автозагрузку**:
   ```bash
   sudo systemctl start postgresql
   sudo systemctl enable postgresql
   ```

3. **Проверка статуса**:
   ```bash
   sudo systemctl status postgresql
   ```

4. **Подключение к PostgreSQL**:
   ```bash
   sudo -u postgres psql
   ```

### 5.2 Создать таблицу и заполнить её тестовыми данными

1. **Создание базы данных**:
   ```sql
   CREATE DATABASE testdb;
   \c testdb
   ```

2. **Создание таблицы**:
   ```sql
   CREATE TABLE employees (
       id SERIAL PRIMARY KEY,
       name VARCHAR(100),
       position VARCHAR(100),
       salary NUMERIC
   );
   ```

3. **Заполнение таблицы тестовыми данными**:
   ```sql
   INSERT INTO employees (name, position, salary) VALUES
   ('Иван Иванов', 'Разработчик', 100000),
   ('Петр Петров', 'Менеджер', 120000),
   ('Сидор Сидоров', 'Аналитик', 90000);
   ```

4. **Проверка данных**:
   ```sql
   SELECT * FROM employees;
   ```

### 5.3 Настроить бэкенд для отображения данных из базы

1. **Установка необходимых библиотек**:
   - Например, для Python:
     ```bash
     pip install psycopg2
     ```

2. **Пример кода на Python для подключения к базе и получения данных**:
   ```python
   import psycopg2

   conn = psycopg2.connect(
       dbname="testdb",
       user="postgres",
       password="yourpassword",
       host="localhost"
   )
   cur = conn.cursor()
   cur.execute("SELECT * FROM employees")
   rows = cur.fetchall()
   for row in rows:
       print(row)
   cur.close()
   conn.close()
   ```

### 5.4 Подключить slave-репликацию

1. **Настройка master-сервера**:
   - В `postgresql.conf`:
     ```conf
     wal_level = replica
     max_wal_senders = 3
     ```
   - В `pg_hba.conf`:
     ```conf
     host replication replicator slave_ip/32 md5
     ```
   - Перезапуск PostgreSQL:
     ```bash
     sudo systemctl restart postgresql
     ```

2. **Создание пользователя для репликации**:
   ```sql
   CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'replicator_password';
   ```

3. **Настройка slave-сервера**:
   - Остановите PostgreSQL на slave:
     ```bash
     sudo systemctl stop postgresql
     ```
   - Создайте резервную копию с master:
     ```bash
     pg_basebackup -h master_ip -D /var/lib/pgsql/data -U replicator -P -v -R
     ```
   - Запустите PostgreSQL на slave:
     ```bash
     sudo systemctl start postgresql
     ```

### 5.5 Освоить процесс резервного копирования и восстановления базы (pg_dump, pg_restore)

1. **Резервное копирование**:
   ```bash
   pg_dump -U postgres -d testdb -F c -b -v -f backup.dump
   ```

2. **Восстановление из резервной копии**:
   ```bash
   pg_restore -U postgres -d newdb -v backup.dump
   ```

### 5.6 Разобраться, что такое WAL, где он хранится и как работает

- **WAL (Write-Ahead Logging)** — это механизм, который записывает все изменения в базу данных в журнал перед тем, как они будут применены к самим данным. Это обеспечивает целостность данных и позволяет восстанавливать базу после сбоев.
- **Где хранится**: WAL-файлы хранятся в каталоге `pg_wal` внутри каталога данных PostgreSQL.
- **Как работает**: Все изменения сначала записываются в WAL, а затем применяются к данным. Это позволяет восстанавливать данные после сбоев, так как WAL содержит все изменения, которые не были применены к данным.

### 5.7 Настроить удалённое подключение к базе (pg_hba.conf, postgresql.conf)

1. **Настройка `postgresql.conf`**:
   - Найдите и измените строку:
     ```conf
     listen_addresses = '*'
     ```

2. **Настройка `pg_hba.conf`**:
   - Добавьте строку для разрешения подключения с определённого IP или диапазона:
     ```conf
     host all all client_ip/32 md5
     ```

3. **Перезапуск PostgreSQL**:
   ```bash
   sudo systemctl restart postgresql
   ```

4. **Проверка подключения**:
   - С удалённого клиента:
     ```bash
     psql -h server_ip -U postgres -d testdb
     ```

Эти шаги помогут вам настроить и использовать PostgreSQL в различных сценариях, включая репликацию, резервное копирование и удалённое подключение.