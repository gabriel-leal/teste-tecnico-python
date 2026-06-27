from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import database
from app.schemas import TaskCreate, TaskUpdate, TaskResponse, TaskStatus
from app.services.task_service import TaskService


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar tarefa",
    description="""
Cria uma nova tarefa.

Regras:
- O título é obrigatório
- Toda tarefa inicia com status **Pendente**
- A tarefa recebe automaticamente data de criação e atualização
""",
    responses={
        201: {"description": "Tarefa criada com sucesso"},
        422: {"description": "Erro de validação dos dados"}
    }
)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(database.get_db)
):
    service = TaskService(db)
    return service.create(payload)


@router.get(
    "",
    response_model=list[TaskResponse],
    summary="Listar tarefas",
    description="""
Lista todas as tarefas não excluídas.

Filtros opcionais:
- Busca parcial por título
- Filtro por status
""",
    responses={
        200: {"description": "Lista de tarefas retornada com sucesso"}
    }
)
def list_tasks(
    title: Optional[str] = Query(
        None,
        description="Busca parcial pelo título. Ex: mercado"
    ),
    status_filter: Optional[TaskStatus] = Query(
        None,
        alias="status",
        description="Filtrar por status: Pendente, Em andamento ou Concluída"
    ),
    db: Session = Depends(database.get_db)
):
    service = TaskService(db)
    return service.list_all(
        title=title,
        status_filter=status_filter
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Buscar tarefa por ID",
    description="Busca uma tarefa específica pelo UUID.",
    responses={
        200: {"description": "Tarefa encontrada"},
        404: {"description": "Tarefa não encontrada"}
    }
)
def get_task_by_id(
    task_id: UUID,
    db: Session = Depends(database.get_db)
):
    service = TaskService(db)
    return service.get_by_id(task_id)


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Atualizar tarefa",
    description="""
Atualiza parcialmente uma tarefa.

Campos opcionais:
- title
- description
- status
""",
    responses={
        200: {"description": "Tarefa atualizada com sucesso"},
        404: {"description": "Tarefa não encontrada"},
        422: {"description": "Erro de validação"}
    }
)
def update_task(
    task_id: UUID,
    payload: TaskUpdate,
    db: Session = Depends(database.get_db)
):
    service = TaskService(db)
    return service.update(task_id, payload)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir tarefa",
    description="""
Realiza exclusão lógica (soft delete).

A tarefa não é removida fisicamente do banco;
apenas recebe a data de exclusão.
""",
    responses={
        204: {"description": "Tarefa excluída com sucesso"},
        404: {"description": "Tarefa não encontrada"}
    }
)
def delete_task(
    task_id: UUID,
    db: Session = Depends(database.get_db)
):
    service = TaskService(db)
    service.soft_delete(task_id)
    return None