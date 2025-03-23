from fastapi import FastAPI, HTTPException
import redis
import os
from pydantic import BaseModel

# Создаем экземпляр FastAPI
app = FastAPI()

# Подключение к Redis
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_password = os.getenv("REDIS_PASSWORD", None)

# Создаем клиент Redis
redis_client = redis.Redis(
    host="192.168.174.138",
    port=6379,
    password="password",
    decode_responses=True  # Автоматически декодировать данные в строки
)

# Модель для входных данных
class Item(BaseModel):
    key: str
    value: str

# Эндпоинт для сохранения данных в Redis
@app.post("/set/")
async def set_item(item: Item):
    """
    Сохраняет значение в Redis по указанному ключу.
    """
    try:
        redis_client.set(item.key, item.value)
        return {"message": f"Key '{item.key}' set successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Эндпоинт для получения данных из Redis
@app.get("/get/{key}")
async def get_item(key: str):
    """
    Получает значение из Redis по указанному ключу.
    """
    try:
        value = redis_client.get(key)
        if value is None:
            raise HTTPException(status_code=404, detail="Key not found")
        return {"key": key, "value": value}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Эндпоинт для удаления данных из Redis
@app.delete("/delete/{key}")
async def delete_item(key: str):
    """
    Удаляет ключ и его значение из Redis.
    """
    try:
        deleted = redis_client.delete(key)
        if deleted == 0:
            raise HTTPException(status_code=404, detail="Key not found")
        return {"message": f"Key '{key}' deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Эндпоинт для получения всех ключей из Redis
@app.get("/keys/")
async def get_all_keys():
    """
    Возвращает список всех ключей в Redis.
    """
    try:
        keys = redis_client.keys("*")  # Получаем все ключи
        return {"keys": keys}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.174.138", port=8111)