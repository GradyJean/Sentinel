from datetime import datetime

from models import OffsetConfig
from storage.database import DatabaseRepository
from sqlmodel import update


class OffsetsService(DatabaseRepository[OffsetConfig]):
    """
    日志采集任务服务
    """
    offsets_id: str = "log_collect"

    def __init__(self):
        super().__init__(OffsetConfig)

    def get(self) -> OffsetConfig:
        """
        获取日志文件偏移量
        """
        return self.get_by_id(self.offsets_id)

    def update(self, config: OffsetConfig):
        """
        保存日志文件偏移量
        """
        now = datetime.now()
        config.id = self.offsets_id
        config.update_time = now
        return self.merge(config)

    def update_offset(self, file_path, offset: int):
        """
        更新日志文件偏移量
        """
        config = self.get()
        config.file_path = file_path
        config.offset = offset
        self.update(config)
