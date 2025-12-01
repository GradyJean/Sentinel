from core.scheduler.task_runner import TaskRunner
from service.offset_service import OffsetsService


class DailyTask(TaskRunner):
    """
    每天定时任务
    """
    task_id = "daily_task"
    offset_service = OffsetsService()

    async def run(self):
        self.rest_offset_count()

    def rest_offset_count(self):
        offset_config = self.offset_service.get()
        offset_config.count = 0
        self.offset_service.update(offset_config)
