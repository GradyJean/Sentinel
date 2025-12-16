from core.scheduler.task_runner import TaskRunner


class ScoreAggregatorTask(TaskRunner):
    """
    评分定时任务
    """
    task_id = "score_aggregator_task"

    def run(self):
        pass
