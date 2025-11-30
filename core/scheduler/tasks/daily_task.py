from core.scheduler.task_runner import TaskRunner


class DailyTask(TaskRunner):
    """
    每天定时任务
    """
    task_id = "daily_task"

    async def run(self):
        pass
