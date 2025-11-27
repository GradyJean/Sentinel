import os
from datetime import datetime
from typing import List

from loguru import logger
from sqlalchemy import func
from sqlmodel import Field
from sqlmodel import select

from config import settings
from core.collector.log_collector import Collector
from core.scheduler.task_runner import TaskRunner
from models.nginx import LogMetaData
from models.storage.database import DatabaseModel
from storage.database import DatabaseRepository


class LogCollectorTask(TaskRunner):
    """
    日志采集任务
    """
    task_id: str = "log_collector"

    def __init__(self):
        self.service = LogCollectorService()
        self.collector = Collector(
            log_path=settings.nginx.log_path,
            call_back=self.batch_save_log,
        )

    async def run(self):
        file_path = settings.nginx.log_path
        if not os.path.exists(file_path):
            logger.error(f"日志文件不存在: {file_path}")
            return
        offsets = self.service.get_offsets()
        offsets = self.collector.run(offsets)
        self.service.save(LogCollector(id="1", file_path=file_path, offsets=offsets))

    def batch_save_log(self, log_metadata: List[LogMetaData]) -> bool:
        """
        批量保存日志
        """
        print(log_metadata)
        return True


class LogCollector(DatabaseModel, table=True):
    """
    日志采集任务配置
    """
    file_path: str = Field(..., description="日志文件路径", unique=True)
    offsets: int = Field(0, description="日志文件偏移量")
    update_time: datetime = Field(default=func.now(), description="更新时间")


class LogCollectorService(DatabaseRepository[LogCollector]):
    """
    日志采集任务服务
    """

    def __init__(self):
        super().__init__(LogCollector)

    def get_offsets(self) -> int:
        """
        获取日志文件偏移量
        """
        with self.get_session() as session:
            record = session.exec(select(LogCollector).where(LogCollector.id == "1")).first()
        if record:
            return record.offsets
        return 0
