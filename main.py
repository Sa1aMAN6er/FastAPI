from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from routers.cash import router as cash_router  # Путь к вашему маршруту
from fastapi.middleware.cors import CORSMiddleware
from routers import cash

from fastapi import FastAPI
from routers import cash

app = FastAPI()
app.include_router(cash.router)

@app.get("/")
def root():
    return {"message": "API работает!"}

