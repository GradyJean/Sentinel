from typing import List

from models.scheduler import TaskScheduler
from service.elasticsearch_service import ElasticsearchService


class TaskSchedulerService(ElasticsearchService[TaskScheduler]):
    """
    任务调度服务
    """

    def __init__(self):
        super().__init__("task_scheduler", TaskScheduler)
