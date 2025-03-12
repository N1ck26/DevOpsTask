1. Устанавливаем postgresql: `sudo apt install -y postgresql postgresql-contrib` (на master и на slave)
2. На master cоздаем бд `CREATE DATABASE test_db;` и подключаемся к ней `\c test_db;` , так же создаим пароль для учетки postgres `alter role postgres with login password 'password';`
3. Создаем тестовую таблицу: `create table Users(id serial primary key, login varchar(50), status_active bool);`
4. Заполянем ее тестовыми значениями:
   ```
   insert into users values (1, 'admin', True)
   insert into users values (2, 'test_login', False)
   ```
5. Пишем бэк для отображения данных из бд. Запускаем его: `uvicorn db:app --reload;`
6. Переходим по url `http://127.0.0.1:8000/users` и видим отображение данных из бд в формате json
7. Настройка slave-репликации для master:

   7.1 На master заходим в конфиг postgresql `/etc/postgresql/16/main/postgresql.conf`:
   ```
   listen_addresses = '*'

   wal_level = replica

   max_wal_senders = 3

   synchronous_commit = on

   synchronous_standby_names = 'replica1'
   ```
   7.2 В файле `/etc/postgresql/14/main/pg_hba.conf` добавляем строку: `host replication  postgres  ip-addr-slave/32  md5`
   
   7.3 Затем ребутаем службу postgres `sudo systemctl restart postgresql`

8. Создаем пользователя для репликации `CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'replicator_password';` 

9. Настройка slave-репликации для slave:

   9.1 На slave останавливаем службу postgresql `sudo systemctl stop postgresql`

   9.2 Удаляем старые данные: `sudo rm -rf /var/lib/postgresql/16/main/*`

   9.3 Создаем резервную копию с master: `pg_basebackup -h 192.168.88.137 -D /var/lib/postgresql/16/main -U replicator -P -R -v`

   9.4 После шага 9.4 будет нужно проверить файл `postgresql.auto.conf` чтобы там присутсвовала запись `primary_conninfo = 'host=<master_ip> port=5432 user=replicator password=replicator_password'`

   9.5 Запускаем службу postgresql `sudo systemctl start postgresql`

10. Проверяем на master: `SELECT * FROM pg_stat_replication;`

11. Проверяем на slave: `SELECT * FROM pg_stat_wal_receiver;`


