1. Установим Redis-server: `sudo apt install redis-server`

2. Изменим в файле: `/etc/redis/redis.conf` значение `bind 127.0.0.1 -::1` на `bind <ip-address-redis-server> -::1`
и так же добавим пароль для входа с помощбью строки `requirepass <password>`

3. Выполним подключение к redis-server с помощью команды `redis-cli -h <ip-address-redis-server> -a <password>`

4. Осуществим подключение redis и python:
   ```
   import redis

   # Создание клиента Redis
   client = redis.Redis(host='127.0.0.1', port=6379, password='ваш_пароль')

   # Установка значения
   client.set('mykey', 'test connection')

   # Получение значения
   value = client.get('mykey')
   print(value.decode('utf-8'))

   # Установка времени жизни ключа
   client.expire('mykey', 10)

   # Закрытие соединения
   client.close()
   ```