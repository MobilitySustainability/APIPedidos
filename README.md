# API Pedidos — Docker e MySQL

# Iniciar

Pré-requisito: Docker Desktop iniciado com containers Linux.

No PowerShell:

powershell
  cd 'Pasta do projeto'
  Copy-Item .env.example .env
  docker compose up -d --build --wait
  docker compose ps

Disponivel em http://localhost:8000, a documentação interativa em http://localhost:8000/docs e a saúde em http://localhost:8000/health. 


# Testar no Postman

1. Abra o Postman e escolha **Import**.
2. Selecione 'postman/API-Pedidos.postman_collection.json'.
3. A variável da coleção 'base_url' já vale 'http://localhost:8000'.

A coleção salva o ID criado automaticamente em 'pedido_id', verifica criação, consulta, listagem, confirmação, cancelamento e respostas 404/422. Cada execução deixa um pedido de teste cancelado no banco. Para enviar requisições individualmente, execute primeiro “02 - Criar pedido”. Se usar Postman Web, selecione o Desktop Agent para acessar localhost.

Exemplo de **POST** 'http://localhost:8000/pedidos', em **Body / raw / JSON**:

json
{
  "cliente": "Carlos",
  "produto": "Mouse",
  "quantidade": 3,
  "valor_unitario": 19.90
}


Resposta: **201**, 'valor_total: 59.7', 'status: "CRIADO"' e ID gerado pelo MySQL.

-----Método----------Rota--------------------Resultado

-----POST----------/pedidos-------------------201 + pedido criado
-----GET-----------/pedidos/{id}--------------200 ou 404
-----GET-----------/pedidos-------------------200 + lista
-----PATCH---------/pedidos/{id}/status-------200 ou 404
-----GET-----------/health--------------------200 ou 503


# Comprovar persistência

Crie um pedido no Postman, anote seu ID e execute:

powershell
docker compose restart pedidos


Depois consulte novamente 'GET /pedidos/{id}': os dados devem ser os mesmos. O script abaixo automatiza a criação, o reinício, a espera e a comparação de todos os campos:

powershell
powershell -ExecutionPolicy Bypass -File scripts/test-persistence.ps1


# Comandos úteis

powershell
docker compose logs --tail 100 pedidos mysql
docker compose stop
docker compose start
docker compose down
docker compose up -d --build --wait


# Organização

- 'app/api': interface HTTP e códigos de resposta.
- 'app/services': regras de negócio e cálculo do total.
- 'app/repositories': consultas parametrizadas e transações MySQL.
- 'app/database.py': conexão por variáveis de ambiente e criação inicial da tabela.
- 'Dockerfile' e 'compose.yaml': aplicação, banco, verificações de saúde e volume.
- 'postman': coleção de testes importável.