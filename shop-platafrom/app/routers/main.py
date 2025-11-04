from fastapi import FastAPI
from .db import engine, Base
from .routers import users, wallet, payments

# criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Payments Sim - API")

app.include_router(users.router)
app.include_router(wallet.router)
app.include_router(payments.router)

@app.get("/")
def root():
    return {"msg": "Payments Sim API running"}
