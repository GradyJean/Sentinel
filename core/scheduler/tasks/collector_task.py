from typing import List

from loguru import logger

from config import settings
from core.collector.log_collector import Collector
from core.scheduler.task_runner import TaskRunner
from models import OffsetConfig
from models.nginx import LogMetaData
from service.log_metadata_service import LogMetaDataService
from service.offset_service import OffsetsService


class LogCollectorTask(TaskRunner):
    """
    日志采集任务
    """
    task_id: str = "log_collector"

    def __init__(self):
        self.offset_service = OffsetsService()
        self.log_metadata_service = LogMetaDataService()
        self.collector = Collector(
            call_back=self.metadata_callback,
        )

    async def run(self):
        file_path = settings.nginx.get_log_path()
        # 文件偏移量
        offset = 0
        # 获取文件偏移量配置
        offset_config = self.offset_service.get()
        if offset_config:
            offset = offset_config.offset
            if offset_config.count == 0:  # count ==0 表示未切换文件 用于收尾昨天日志
                file_path = offset_config.file_path
        else:
            offset_config = OffsetConfig(
                file_path=file_path,
                offset=offset,
                count=0
            )
            # 先保存
            self.offset_service.update(offset_config)
        # 文件采集并返回偏移量
        offset = self.collector.start(file_path=file_path, offset=offset)
        # 保存文件偏移量
        offset_config.file_path = file_path
        offset_config.offset = offset
        offset_config.count += 1
        self.offset_service.update(offset_config)

    def metadata_callback(self, metadata_list: List[LogMetaData], file_path: str, offset: int) -> bool:
        save_status = self.log_metadata_service.batch_insert(metadata_list)
        if save_status:
            # 随时保存文件偏移量 防止程序中断丢失数据
            self.offset_service.update_offset(file_path=file_path, offset=offset)
            logger.info(f"log metadata save success: {len(metadata_list)}")
            return True
        return False
