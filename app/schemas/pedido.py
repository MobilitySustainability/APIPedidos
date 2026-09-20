"""Schemas de entrada e saída da API (validação HTTP com Pydantic)"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict

from app.models.pedido import StatusPedido


class PedidoCreate(BaseModel):
    """Entrada do POST /pedidos."""

    model_config = ConfigDict(str_strip_whitespace=True)

    cliente: str = Field(..., min_length=1, max_length=255, description="Identificação textual do cliente")
    produto: str = Field(..., min_length=1, max_length=255, description="Identificação textual do produto")
    quantidade: int = Field(..., gt=0, le=2147483647, description="Quantidade solicitada (> 0)")
    valor_unitario: Decimal = Field(..., gt=0, max_digits=12, decimal_places=2, description="Preço de uma unidade (> 0, até 2 casas decimais)")


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

    model_config = ConfigDict(from_attributes=True)
