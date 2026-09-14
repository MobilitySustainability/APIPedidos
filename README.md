# API Pedidos

## Estrutura mínima p/ testar

```
/app
├── main.py
├── api/pedidos.py
├── services/pedido_service.py
├── repositories/pedido_repository.py
├── models/pedido.py
├── schemas/pedido.py
└── data/pedidos_mock.json
requirements.txt
README.md
```

## Endpoints

| Método | Rota | Resposta |
|---|---|---|
| POST | `/pedidos` | 201 + pedido criado |
| GET | `/pedidos/{id}` | 200 / 404 |
| GET | `/pedidos` | 200 lista |
| PATCH | `/pedidos/{id}/status` | 200 / 404 |
| GET | `/health` | `{"status": "ok"}` |

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
# Docs: http://localhost:8000/docs
```
