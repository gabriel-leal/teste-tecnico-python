# To-Do API

API REST simples para gerenciar tarefas, feita com FastAPI, SQLAlchemy e PostgreSQL.

## Requisitos

- Python 3.12+
- Docker e Docker Compose

## Variáveis de ambiente

Crie o arquivo `.env` a partir do exemplo:

```bash
cp .env.example .env
```

No Docker, o `DATABASE_URL` deve usar o host `db`, como já está no `.env.example`.

## Rodando com Docker

```bash
docker compose up --build
```

A API fica disponível em:

```text
http://localhost:8000
```

Para parar:

```bash
docker compose down
```

## Documentação da API

Com a API rodando, acesse:

- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

Também existe uma collection do Postman em:

```text
docs/todo-api.postman_collection.json
```

## Rodando os testes

Instale as dependências:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Depois rode:

```bash
pytest
```

Se for rodar os testes fora do Docker, mantenha o `.env` criado, pois a aplicação precisa do `DATABASE_URL` ao iniciar.

## Rotas

- `GET /` - health check
- `POST /tasks` - cria uma tarefa
- `GET /tasks` - lista tarefas
- `GET /tasks?title=...&status=...` - lista com filtros
- `GET /tasks/{task_id}` - busca por ID
- `PATCH /tasks/{task_id}` - atualiza uma tarefa
- `DELETE /tasks/{task_id}` - remove uma tarefa com soft delete
