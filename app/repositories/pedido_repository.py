"""Camada de dados (Repository)"""

from datetime import datetime
from pathlib import Path
import json
from typing import Dict, List, Optional

from app.models.pedido import Pedido, StatusPedido

# Armazenamento em memória, semeado pelo JSON mockado.
_db: Dict[int, Pedido] = {}
_next_id: int = 1

MOCK_PATH = Path(__file__).resolve().parents[1] / "data" / "pedidos_mock.json"


def _carregar_mock() -> None:
    """Carrega app/data/pedidos_mock.json para a memória (só p/ teste)."""
    global _db, _next_id
    if _db:
        return
    try:
        dados = json.loads(MOCK_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return
    for item in dados:
        pedido = Pedido(
            id=item["id"],
            cliente=item["cliente"],
            produto=item["produto"],
            quantidade=item["quantidade"],
            valor_unitario=item["valor_unitario"],
            valor_total=item["valor_total"],
            status=StatusPedido(item["status"]),
            data_criacao=datetime.fromisoformat(item["data_criacao"]),
        )
        _db[pedido.id] = pedido
    if _db:
        _next_id = max(_db.keys()) + 1


_carregar_mock()


def reset_store() -> None:
    """Util para testes. Recarrega o mock (descarta alterações)."""
    global _db, _next_id
    _db = {}
    _next_id = 1
    _carregar_mock()


def criar(pedido: Pedido) -> Pedido:
    """Persiste um novo pedido e retorna com id gerado."""
    global _next_id
    pedido.id = _next_id
    _next_id += 1
    _db[pedido.id] = pedido
    return pedido

    # TODO (PostgreSQL):
    #   db.add(pedido_model)
    #   db.commit()
    #   db.refresh(pedido_model)
    #   return pedido_model


def buscar_por_id(pedido_id: int) -> Optional[Pedido]:
    """Retorna o pedido pelo id ou None se não existir."""
    return _db.get(pedido_id)

    # TODO (PostgreSQL):
    #   return db.query(PedidoModel).filter(PedidoModel.id == pedido_id).first()


def listar() -> List[Pedido]:
    """Retorna a coleção de pedidos existentes."""
    return list(_db.values())

    # TODO (PostgreSQL):
    #   return db.query(PedidoModel).all()


def atualizar_status(pedido_id: int, novo_status: StatusPedido) -> Optional[Pedido]:
    """Atualiza apenas o estado do pedido. Retorna None se não existir."""
    pedido = _db.get(pedido_id)
    if pedido is None:
        return None
    pedido.status = novo_status
    return pedido

    # TODO (PostgreSQL):
    #   pedido = buscar_por_id(db, pedido_id)
    #   if not pedido: return None
    #   pedido.status = novo_status
    #   db.commit()
    #   db.refresh(pedido)
    #   return pedido
