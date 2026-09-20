"""Persistência de pedidos no MySQL, com consultas parametrizadas."""
from datetime import timezone
from app.database import connection
from app.models.pedido import Pedido, StatusPedido


def _pedido(row):
    if row is None:
        return None
    row['status'] = StatusPedido(row['status'])
    row['data_criacao'] = row['data_criacao'].replace(tzinfo=timezone.utc)
    return Pedido(**row)


def criar(pedido):
    with connection() as db, db.cursor() as cursor:
        cursor.execute('''INSERT INTO pedidos
            (cliente, produto, quantidade, valor_unitario, valor_total, status, data_criacao)
            VALUES (%s, %s, %s, %s, %s, %s, %s)''',
            (pedido.cliente, pedido.produto, pedido.quantidade, pedido.valor_unitario,
             pedido.valor_total, pedido.status.value,
             pedido.data_criacao.astimezone(timezone.utc).replace(tzinfo=None)))
        pedido.id = cursor.lastrowid
    return pedido


def buscar_por_id(pedido_id):
    with connection() as db, db.cursor() as cursor:
        cursor.execute('SELECT * FROM pedidos WHERE id = %s', (pedido_id,))
        return _pedido(cursor.fetchone())


def listar():
    with connection() as db, db.cursor() as cursor:
        cursor.execute('SELECT * FROM pedidos ORDER BY id')
        return [_pedido(row) for row in cursor.fetchall()]


def atualizar_status(pedido_id, novo_status):
    with connection() as db, db.cursor() as cursor:
        cursor.execute('UPDATE pedidos SET status = %s WHERE id = %s',
                       (novo_status.value, pedido_id))
        cursor.execute('SELECT * FROM pedidos WHERE id = %s', (pedido_id,))
        return _pedido(cursor.fetchone())
