from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4(), index=True)

    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)

    status = Column(String(30), nullable=False, default="Pendente")

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    deleted_at = Column(DateTime, nullable=True)