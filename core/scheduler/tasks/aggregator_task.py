from core.scheduler.task_runner import TaskRunner
from service.aggregator_service import AccessIpAggregationService
from service.log_metadata_service import LogMetaDataBatchService


class LogAggregatorTask(TaskRunner):
    task_id: str = "log_aggregator"
    log_metadata_batch_service = LogMetaDataBatchService()
    access_ip_aggregation_service = AccessIpAggregationService()

    async def run(self):
        pass
