"""Inicialização do FastAPI (app/main.py)."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pymysql import MySQLError
from app.database import connection, initialize

from app.api.pedidos import router as pedidos_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="API Pedidos",
    description="Trabalho 1 - Desenvolvimento de Sistemas Distribuídos (UNIP)",
    version="1.0.0",
)

app.include_router(pedidos_router)


@app.get("/health", tags=["saúde"])
def health():
    """Endpoint de saúde. Resposta mínima: { "status": "ok" }."""
    try:
        with connection() as db, db.cursor() as cursor:
            cursor.execute("SELECT 1")
    except MySQLError:
        raise HTTPException(status_code=503, detail="Banco de dados indisponível")
    return {"status": "ok"}


@app.get("/", tags=["saúde"])
def root():
    return {"message": "API Pedidos operacional. Use /docs para testar."}
