from fastapi import FastAPI
from app.database import Base
from app.database import engine
from app import models

app = FastAPI(
    title = "Travel Planner API",
    version = '1.0.0',
)

@app.on_event('startup')
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {
        'message': "Travel Planner API"
    }
