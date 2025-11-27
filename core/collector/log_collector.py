import os
from typing import Callable, List

from models.nginx import LogMetaData


class Collector:
    """
    日志采集类

    """
    __is_running = False
    __log_path: str
    __call_back: Callable[[List[LogMetaData]], bool]
    __batch_size: int = 1000

    def __init__(self, log_path: str, call_back: Callable[[List[LogMetaData]], bool], batch_size: int = 1000):
        """
        初始化日志采集类
        Args:
            log_path 日志文件路径
            call_back 日志回调函数
            batch_size 批量写入大小
        """
        if not log_path or not os.path.exists(log_path):
            raise ValueError("log_path is empty or file does not exist")
        if not call_back:
            raise ValueError("call_back is empty")

        self.__log_path = log_path
        self.__call_back = call_back
        self.__batch_size = batch_size

    def run(self, offsets: int = 0) -> int:
        """
            运行日志采集
            return offsets
        """
        batch_log_metadata: List[LogMetaData] = []
        with open(self.__log_path, 'r', encoding="utf-8") as file:
            self.__is_running = True
            # 定位到指定偏移量
            file.seek(offsets)
            for line in file:
                try:
                    log_metadata = LogMetaData.parse(line)
                except ValueError:
                    continue
                batch_log_metadata.append(log_metadata)
                # 停止运行
                if not self.__is_running:
                    break
                # 批量写入
                if len(batch_log_metadata) >= self.__batch_size:
                    self.__call_back(batch_log_metadata)
                    batch_log_metadata.clear()
            # 写入剩余数据
            if len(batch_log_metadata) > 0:
                self.__call_back(batch_log_metadata)
                batch_log_metadata.clear()
            # 运行状态更新
            self.__is_running = False
            return file.tell()

    def stop(self):
        """
        停止日志采集
        :return:
        """
        self.__is_running = False

    def status(self) -> bool:
        """
        获取运行状态
        :return:
        """
        return self.__is_running
