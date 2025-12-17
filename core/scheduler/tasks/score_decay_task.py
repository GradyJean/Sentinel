import datetime

from core.scheduler.task_runner import TaskRunner
from manager.ip_score_manager import IpSummaryManager
from manager.system_config_manager import SystemConfigManager


class ScoreDecayTask(TaskRunner):
    """
    分数衰减定时任务
    """
    task_id = "score_decay_task"
    ip_summary_manager = IpSummaryManager()
    system_config_manager = SystemConfigManager()
    BASE_DECAY_SCORE = 10

    def run(self):
        system_config = self.system_config_manager.system_config
        factor_fixed = system_config["score_decay_factor_fixed"]
        actor_dynamic = system_config["score_decay_factor_dynamic"]
        factor_feature = system_config["score_decay_factor_feature"]
        dec_fixed = self.BASE_DECAY_SCORE * factor_fixed
        dec_dynamic = self.BASE_DECAY_SCORE * actor_dynamic
        dec_feature = self.BASE_DECAY_SCORE * factor_feature
        self.update_score(dec_fixed, dec_dynamic, dec_feature)

    def update_score(self, dec_fixed, dec_dynamic, dec_feature):
        es_client = self.ip_summary_manager.get_client()
        index = self.ip_summary_manager.index
        body = {
            "query": {
                "bool": {
                    "should": [
                        {"range": {"score_fixed": {"gt": 0}}},
                        {"range": {"score_dynamic": {"gt": 0}}},
                        {"range": {"score_feature": {"gt": 0}}},
                    ],
                    "minimum_should_match": 1
                }
            },
            "script": {
                "lang": "painless",
                "source": """
                    ctx._source.score_fixed =
                      Math.max(0, ctx._source.score_fixed - params.dec_fixed);

                    ctx._source.score_dynamic =
                      Math.max(0, ctx._source.score_dynamic - params.dec_dynamic);

                    ctx._source.score_feature =
                      Math.max(0, ctx._source.score_feature - params.dec_feature);

                    ctx._source.last_update = params.now;
                """,
                "params": {
                    "dec_fixed": dec_fixed,
                    "dec_dynamic": dec_dynamic,
                    "dec_feature": dec_feature,
                    "now": datetime.datetime.now()
                }
            },
            "conflicts": "proceed"
        }
        es_client.update_by_query(
            index=index,
            body=body,
            refresh=True,
        )
