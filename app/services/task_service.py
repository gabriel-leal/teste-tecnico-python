from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Task
from app.schemas import TaskCreate, TaskUpdate, TaskStatus


class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: TaskCreate) -> Task:
        task = Task(
            title=payload.title,
            description=payload.description,
            status=payload.status.value
        )

        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        return task

    def list_all(
        self,
        title: Optional[str] = None,
        status_filter: Optional[TaskStatus] = None
    ) -> list[Task]:
        query = self.db.query(Task).filter(Task.deleted_at.is_(None))

        if title:
            query = query.filter(Task.title.ilike(f"%{title}%"))

        if status_filter:
            query = query.filter(Task.status == status_filter.value)

        return query.order_by(Task.created_at.desc()).all()

    def get_by_id(self, task_id: UUID) -> Task:
        task = (
            self.db.query(Task)
            .filter(
                Task.id == task_id,
                Task.deleted_at.is_(None)
            )
            .first()
        )

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarefa não encontrada"
            )

        return task

    def update(self, task_id: UUID, payload: TaskUpdate) -> Task:
        task = self.get_by_id(task_id)

        update_data = payload.model_dump(exclude_unset=True)

        if "title" in update_data:
            task.title = update_data["title"]

        if "description" in update_data:
            task.description = update_data["description"]

        if "status" in update_data:
            task.status = update_data["status"].value

        self.db.commit()
        self.db.refresh(task)

        return task

    def soft_delete(self, task_id: UUID) -> None:
        task = self.get_by_id(task_id)

        task.deleted_at = datetime.now(timezone.utc)

        self.db.commit()