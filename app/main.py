"""Inicialização do FastAPI (app/main.py)."""

from fastapi import FastAPI

from app.api.pedidos import router as pedidos_router

app = FastAPI(
    title="API Pedidos",
    description="Trabalho 1 - Desenvolvimento de Sistemas Distribuídos (UNIP)",
    version="1.0.0",
)

app.include_router(pedidos_router)


@app.get("/health", tags=["saúde"])
def health():
    """Endpoint de saúde. Resposta mínima: { "status": "ok" }."""
    return {"status": "ok"}


@app.get("/", tags=["saúde"])
def root():
    return {"message": "API Pedidos operacional. Use /docs para testar."}
