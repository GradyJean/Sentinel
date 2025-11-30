from datetime import datetime

from models.nginx import LogMetaData
from storage.document import ElasticSearchRepository


class LogMetaDataService(ElasticSearchRepository[LogMetaData]):
    """
    日志服务
    """

    def __init__(self):
        super().__init__("nginx_log_metadata", LogMetaData)

    def create_daily_index(self):
        """
        获取当前索引
        :return:
        """
        now = datetime.now()
        index_name = f"nginx_log_metadata_{now.strftime('%Y_%m_%d')}"
        # 创建索引
        self.create_index(index_name, self.get_index_template("nginx_log_metadata"))
