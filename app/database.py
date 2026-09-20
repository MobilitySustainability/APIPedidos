"""Conexão e criação inicial das tabelas no MySQL."""
import os
from contextlib import contextmanager
import pymysql
from pymysql.cursors import DictCursor


@contextmanager
def connection():
    db = pymysql.connect(
        host=os.environ.get("DB_HOST", "mysql"),
        port=int(os.environ.get("DB_PORT", "3306")),
        user=os.environ["MYSQL_USER"], password=os.environ["MYSQL_PASSWORD"],
        database=os.environ["MYSQL_DATABASE"], charset="utf8mb4",
        cursorclass=DictCursor, connect_timeout=5, read_timeout=10, write_timeout=10,
    )
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def initialize():
    with connection() as db, db.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pedidos (
                id BIGINT PRIMARY KEY AUTO_INCREMENT,
                cliente VARCHAR(255) NOT NULL,
                produto VARCHAR(255) NOT NULL,
                quantidade INT NOT NULL,
                valor_unitario DECIMAL(12,2) NOT NULL,
                valor_total DECIMAL(22,2) NOT NULL,
                status ENUM('CRIADO', 'CONFIRMADO', 'CANCELADO') NOT NULL,
                data_criacao DATETIME(6) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
