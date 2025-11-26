import sys

from loguru import logger


def setup_logger():
    # 清空默认的 handler（默认只打到 stdout）
    logger.remove()
    # 控制台输出
    logger.add(sys.stdout, level="DEBUG", colorize=True,
               format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                      "<level>{level: <8}</level> | "
                      "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                      "<level>{message}</level>")
    # 文件输出（按天滚动保存）
    logger.add("./logs/sentinel.log", rotation="1 day", retention="7 days",
               encoding="utf-8", enqueue=True, level="INFO")
