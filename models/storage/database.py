import uuid
from typing import Optional

from sqlmodel import SQLModel, Field


class DatabaseModel(SQLModel):
    """
    数据库模型
    """
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
