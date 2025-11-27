from datetime import datetime

from sqlalchemy import func
from sqlmodel import Field

from models.storage.database import DatabaseModel


class Offsets(DatabaseModel, table=True):
    """
    日志采集任务配置
    """
    file_path: str = Field(..., description="日志文件路径", unique=True)
    offsets: int = Field(0, description="日志文件偏移量")
    update_time: datetime = Field(default=func.now(), description="更新时间")
