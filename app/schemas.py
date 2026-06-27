from datetime import datetime
from zoneinfo import ZoneInfo
from enum import Enum
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict, field_serializer



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
    
    @field_serializer("created_at", "updated_at", "deleted_at")
    def serialize_datetime_brazil(self, value: Optional[datetime]):
        if value is None:
            return None

        return value.astimezone(
            ZoneInfo("America/Sao_Paulo")
        ).isoformat()

    model_config = ConfigDict(from_attributes=True)