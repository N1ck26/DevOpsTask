import os
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, select, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Session

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@db/test_db")

# Настройка подключения к БД
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Определение модели
class User(Base):
    __tablename__ = "users_list"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(50))
    status_active = Column(Boolean)

# Создание таблицы (если не создана)
Base.metadata.create_all(bind=engine)

# Зависимость для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Инициализация FastAPI
app = FastAPI()

# Эндпоинт для получения всех пользователей
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
