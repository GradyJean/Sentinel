from typing import Optional

from models.scheduler import TaskScheduler
from storage.document import ElasticSearchRepository


class TaskSchedulerService(ElasticSearchRepository[TaskScheduler]):
    """
    任务调度服务
    """

    def __init__(self):
        super().__init__("task_scheduler", TaskScheduler)

    def get_by_task_id(self, task_id: str) -> Optional[TaskScheduler]:
        query = {
            "query": {
                "match": {
                    "task_id": task_id
                }
            }
        }
        result = self.get_client().search(index=self.index, body=query)
        if result.get("hits").get("total").get("value") == 0:
            return None
        record = TaskScheduler(**result.get("hits").get("hits")[0].get("_source"))
        record.id = result.get("hits").get("hits")[0].get("_id")
        return record
