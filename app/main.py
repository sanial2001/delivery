from fastapi import FastAPI
from .routers import auth, orders
from . import models
from .db import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(orders.router)
