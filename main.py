import json

from core.collector.tailer import LogTailer, Log


def print_log(log: Log) -> bool:
    print(log)
    return True


log_path = "data/logs/las.ac.cn_access_2025-11-04.log"
logTailer = LogTailer(log_path=log_path, call_back=print_log)
print(logTailer.collect_cycle(duration=2, offset=0))