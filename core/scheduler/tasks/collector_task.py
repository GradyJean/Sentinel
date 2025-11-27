import os
from typing import List

from loguru import logger
from sqlmodel import select

from config import settings
from core.collector.log_collector import Collector
from core.scheduler.task_runner import TaskRunner
from models.log import Offsets
from models.nginx import LogMetaData
from storage.database import DatabaseRepository
from storage.document import ElasticSearchRepository


class LogCollectorTask(TaskRunner):
    """
    日志采集任务
    """
    task_id: str = "log_collector"
    offsets_id: str = "log_collector_offsets"

    def __init__(self):
        self.offsetService = OffsetsService()
        self.collector = Collector(
            log_path=settings.nginx.log_path,
            call_back=self.batch_save_log,
        )

    async def run(self):
        file_path = settings.nginx.log_path
        if not os.path.exists(file_path):
            logger.error(f"日志文件不存在: {file_path}")
            return
        offsets = self.offsetService.get_offsets(self.offsets_id)
        offsets = self.collector.run(offsets)
        self.offsetService.save(Offsets(id=self.offsets_id, file_path=file_path, offsets=offsets))

    def batch_save_log(self, log_metadata: List[LogMetaData]) -> bool:
        """
        批量保存日志
        """
        for log_metadata in log_metadata:
            print(log_metadata)
        return True


class OffsetsService(DatabaseRepository[Offsets]):
    """
    日志采集任务服务
    """

    def __init__(self):
        super().__init__(Offsets)

    def get_offsets(self, id: str) -> int:
        """
        获取日志文件偏移量
        """
        with self.get_session() as session:
            record = session.exec(select(Offsets).where(Offsets.id == id)).first()
        if record:
            return record.offsets
        return 0


class LogService(ElasticSearchRepository[LogMetaData]):
    """
    日志服务
    """

    def __init__(self):
        super().__init__("",LogMetaData)
