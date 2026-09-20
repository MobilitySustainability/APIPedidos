"""Modelo persistente de Pedido"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from decimal import Decimal


class StatusPedido(str, Enum):
    CRIADO = "CRIADO"
    CONFIRMADO = "CONFIRMADO"
    CANCELADO = "CANCELADO"


@dataclass
class Pedido:
    id: int
    cliente: str
    produto: str
    quantidade: int
    valor_unitario: Decimal
    valor_total: Decimal
    status: StatusPedido = StatusPedido.CRIADO
    data_criacao: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
