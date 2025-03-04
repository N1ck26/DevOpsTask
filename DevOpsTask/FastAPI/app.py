from fastapi import FastAPI
import uvicorn
import asyncio

# Создаём два FastAPI-приложения
app_9999 = FastAPI()
app_9998 = FastAPI()

# Определяем маршруты для порта 9999
@app_9999.get("/app11")
def app11():
    return {"test": "app11"}

@app_9999.get("/app12")
def app12():
    return {"test": "app12"}

# Определяем маршруты для порта 9998
@app_9998.get("/app21")
def app21():
    return {"test": "app21"}

@app_9998.get("/app22")
def app22():
    return {"test": "app22"}

# Функция для одновременного запуска двух серверов
async def main():
    server1 = uvicorn.Server(uvicorn.Config(app_9999, host="127.0.0.1", port=9999, workers=2))
    server2 = uvicorn.Server(uvicorn.Config(app_9998, host="127.0.0.1", port=9998, workers=2))

    await asyncio.gather(
        server1.serve(),
        server2.serve()
    )

if __name__ == "__main__":
    asyncio.run(main())


