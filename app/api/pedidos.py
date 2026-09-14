"""Camada de API (Controller)"""

from typing import List

from fastapi import APIRouter, HTTPException, status

from app.schemas.pedido import PedidoCreate, PedidoResponse, PedidoUpdateStatus
from app.services import pedido_service

router = APIRouter(prefix="/pedidos", tags=["pedidos"])


@router.post("", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def criar_pedido(dados: PedidoCreate):
    """Cria um pedido. A aplicação calcula valor_total e define status CRIADO."""
    pedido = pedido_service.criar_pedido(dados)
    return pedido


@router.get("", response_model=List[PedidoResponse])
def listar_pedidos():
    """Retorna a coleção de pedidos existentes."""
    return pedido_service.listar_pedidos()


@router.get("/{pedido_id}", response_model=PedidoResponse)
def consultar_pedido(pedido_id: int):
    """Retorna 200 quando existe, 404 quando não existe. Não altera estado."""
    pedido = pedido_service.buscar_pedido(pedido_id)
    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado",
        )
    return pedido


@router.patch("/{pedido_id}/status", response_model=PedidoResponse)
def alterar_status(pedido_id: int, dados: PedidoUpdateStatus):
    """Atualiza apenas o estado do pedido."""
    pedido = pedido_service.alterar_status(pedido_id, dados.status)
    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado",
        )
    return pedido
