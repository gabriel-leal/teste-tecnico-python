from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict



class TaskStatus(str, Enum):
    pending = "Pendente"
    in_progress = "Em andamento"
    completed = "Concluída"


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.pending


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=150)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


class TaskResponse(TaskBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)