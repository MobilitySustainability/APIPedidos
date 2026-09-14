"""Schemas de entrada e saída da API (validação HTTP com Pydantic)"""

from datetime import datetime

from pydantic import BaseModel, Field

from app.models.pedido import StatusPedido


class PedidoCreate(BaseModel):
    """Entrada do POST /pedidos."""

    cliente: str = Field(..., min_length=1, description="Identificação textual do cliente")
    produto: str = Field(..., min_length=1, description="Identificação textual do produto")
    quantidade: int = Field(..., gt=0, description="Quantidade solicitada (> 0)")
    valor_unitario: float = Field(..., gt=0, description="Preço de uma unidade (> 0)")


class PedidoUpdateStatus(BaseModel):
    """Entrada do PATCH /pedidos/{id}/status."""

    status: StatusPedido = Field(..., description="Novo estado do pedido")


class PedidoResponse(BaseModel):
    """Saída da API (pedido criado / consultado / listado)."""

    id: int
    cliente: str
    produto: str
    quantidade: int
    valor_unitario: float
    valor_total: float
    status: StatusPedido
    data_criacao: datetime

    class Config:
        from_attributes = True
