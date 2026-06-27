from fastapi import FastAPI

from app.database import Base, database
from app.models import Task
from app.routes.tasks import router as task_router
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import Base, database


tags_metadata = [
    {
        "name": "Tasks",
        "description": "Operações para criar, listar, buscar, atualizar e excluir tarefas."
    },
    {
        "name": "Health Check",
        "description": "Endpoint para verificar se a API está rodando."
    }
]

app = FastAPI(
    title="To-Do API",
    description="""
API REST para gerenciamento de tarefas.

### Recursos

- Criar tarefas
- Listar tarefas
- Buscar tarefa por ID
- Atualizar tarefa
- Excluir tarefa com soft delete
- Filtrar por status
- Buscar por título

### Status disponíveis

- Pendente
- Em andamento
- Concluída
""",
    version="1.0.0",
    contact={
        "name": "Gabriel Leal Menezes",
    },
    openapi_tags=tags_metadata
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=database.engine)
    yield


app = FastAPI(
    title="To-Do API",
    lifespan=lifespan
)

app.include_router(task_router)



@app.get(
    "/",
    tags=["Health Check"],
    summary="Health Check",
    description="Verifica se a API está rodando corretamente."
)
def health_check():
    return {
        "status": "ok",
        "message": "To-Do API rodando"
    }