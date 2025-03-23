import redis

# Создание клиента Redis
client = redis.Redis(host='192.168.174.138', port=6379, password='password')

# Установка значения
client.set('mykey', 'test connection')

# Получение значения
value = client.get('test_key')
print(value.decode('utf-8'))

# Установка времени жизни ключа
#client.expire('mykey', 10)

# Закрытие соединения
client.close()