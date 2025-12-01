import datetime
from typing import List

from loguru import logger

from config import settings
from core.collector.log_collector import Collector
from core.scheduler.task_runner import TaskRunner
from models.log import LogMetaData
from service.log_metadata_service import LogMetaDataService, LogMetaDataBatchService
from service.offset_service import OffsetsService


class LogCollectorTask(TaskRunner):
    """
    日志采集任务
    """
    task_id: str = "log_collector"

    def __init__(self):
        self.offset_service = OffsetsService()
        self.log_metadata_service = LogMetaDataService()
        self.log_metadata_batch_service = LogMetaDataBatchService()
        self.collector = Collector(
            call_back=self.metadata_callback,
        )

    async def run(self):
        """
            初始计数 从1开始 1表示从今天的文件开始
            0表示昨天日志 用于收尾昨天日志
            count =1 的时候offset 为0 表示从文件头开始
            count 字段 由daily_task 任务更新
        """
        now = datetime.datetime.now()
        file_path = settings.nginx.get_log_path()

        # 创建索引(如果不存在)
        index_name = f"log_metadata_{now.strftime('%Y_%m_%d')}"
        template = self.log_metadata_service.get_index_template("nginx_log_metadata")
        self.log_metadata_service.create_index(index_name, template)

        # 获取文件偏移量配置
        offset_config = self.offset_service.get()
        offset = offset_config.offset
        # count ==0 表示未切换文件 用于收尾昨天日志
        if offset_config.count == 0:
            file_path = offset_config.file_path
            self.log_metadata_service.index = offset_config.index_name
        if offset_config.count == 1:  # count > 1 表示已经切换文件
            offset = 0
            self.log_metadata_service.index = index_name

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
