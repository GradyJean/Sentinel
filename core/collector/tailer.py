import os
from datetime import datetime, timedelta
from typing import Callable, IO, Optional

from pydantic import BaseModel


class Log(BaseModel):
    """
    Log 用于保存 Nginx 日志信息
    """
    remote_addr: Optional[str]
    remote_user: Optional[str]
    time_local: Optional[str]
    request: Optional[str]
    status: Optional[int]
    body_bytes_sent: Optional[int]
    http_referer: Optional[str]
    http_user_agent: Optional[str]


class LogTailer:
    log_path: str
    call_back: Callable[[Log], bool]

    def __init__(self, log_path: str, call_back: Callable[[Log], bool]):
        if not os.path.exists(log_path):
            raise FileNotFoundError(f"Log file {log_path} not found")
        self.log_path = log_path
        if not callable(call_back):
            raise TypeError("call_back must be a callable function")
        self.call_back = call_back

    """
    LogTailer 用于从 Nginx access.log 中实时读取新增日志内容
    """

    def collect_cycle(self, offset: int = 0, duration: int = 60) -> int:
        """
        从日志文件中读取最近 duration 秒的日志内容
        :param offset 偏移量 默认0 从头开始读
        :param duration 处理时间 单位秒
        :return: int 返回最新文件偏移量
        """
        end_time = datetime.now() + timedelta(seconds=duration)
        with open(self.log_path, 'rb') as file:
            last_line_offset = self.get_last_line_offset(file)
            if last_line_offset == offset:
                return last_line_offset
            file.seek(offset)
            for line in file:
                if datetime.now() >= end_time:
                    break
                complete_status = self.call_back(self.parse_log_line(line.decode("utf-8")))
            return last_line_offset

    @staticmethod
    def parse_log_line(line: str) -> Log | None:
        """
        解析日志行
        '$remote_addr||
        $remote_user||
        $time_local||
        $request||
        $status||
        $body_bytes_sent||
        $http_referer||
        $http_user_agent';
        :param line: 日志行
        :return: Log 对象
        """
        if len(line) == 0 or not line:
            return None
        data = line.split("||")
        if len(data) != 8:
            raise ValueError("Invalid log line error", line)
        return Log(
            remote_addr=data[0] if data[0] else None,
            remote_user=data[1] if data[1] else None,
            time_local=data[2] if data[2] else None,
            request=data[3] if data[3] else None,
            status=int(data[4]) if data[4] else 0,
            body_bytes_sent=int(data[5]) if data[5] else 0,
            http_referer=data[6] if data[6] else None,
            http_user_agent=data[7] if data[7] else None,
        )

    @staticmethod
    def get_last_line_offset(file: IO):
        """
        获取文件最后一行的偏移量（必须是完整行）
        如果最后一行不完整，则使用上一行作为偏移量
        如果没有内容则返回0
        """
        # 移动到文件末尾
        file.seek(0, 2)  # SEEK_END
        file_size = file.tell()

        if file_size == 0:
            return 0

        # 从文件末尾开始向前查找换行符
        pos = file_size - 1

        # 如果最后一个字符是换行符，我们需要找到倒数第二个换行符
        file.seek(pos)
        if file.read(1) == b'\n':
            # 跳过末尾的换行符
            pos -= 1

        # 查找前一个换行符
        while pos >= 0:
            file.seek(pos)
            if file.read(1) == b'\n':
                # 找到了换行符，下一个是完整行的开始
                return pos + 1
            pos -= 1

        # 如果没有找到换行符，说明整个文件只有一行
        return 0
