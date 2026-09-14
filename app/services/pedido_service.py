"""Camada de lógica (Service)"""

from datetime import datetime, timezone
from typing import List, Optional

from app.models.pedido import Pedido, StatusPedido
from app.repositories import pedido_repository
from app.schemas.pedido import PedidoCreate


def criar_pedido(dados: PedidoCreate) -> Pedido:
    """Cria um pedido com regras de negócio e persiste via repository."""
    valor_total = dados.quantidade * dados.valor_unitario

    pedido = Pedido(
        id=0,
        cliente=dados.cliente.strip(),
        produto=dados.produto.strip(),
        quantidade=dados.quantidade,
        valor_unitario=dados.valor_unitario,
        valor_total=valor_total,
        status=StatusPedido.CRIADO,
        data_criacao=datetime.now(timezone.utc),
    )
    return pedido_repository.criar(pedido)


def buscar_pedido(pedido_id: int) -> Optional[Pedido]:
    """Consulta um pedido sem alterar seu estado."""
    return pedido_repository.buscar_por_id(pedido_id)


def listar_pedidos() -> List[Pedido]:
    """Lista todos os pedidos."""
    return pedido_repository.listar()


def alterar_status(pedido_id: int, novo_status: StatusPedido) -> Optional[Pedido]:
    """Valida existência e atualiza apenas o estado do pedido."""
    return pedido_repository.atualizar_status(pedido_id, novo_status)
