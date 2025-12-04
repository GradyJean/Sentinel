from typing import List

from models.aggregator import AccessIpAggregation, KeyValue, ExtendedStats, StdDeviationBound
from storage.document import ElasticSearchRepository


class AccessIpAggregationService(ElasticSearchRepository[AccessIpAggregation]):
    """
    访问IP聚合服务
    """
    PREFIX = "log_metadata_"

    def __init__(self):
        super().__init__("access_ip_aggregation", AccessIpAggregation)

    def query_access_ip_aggregation(self, batch_id: str) -> List[AccessIpAggregation]:
        index_name = f"{self.PREFIX}{batch_id[:10]}"
        query = {
            "from": 0,
            "size": 0,
            "query": {"term": {"batch_id": batch_id}},
            "aggregations": {
                "ip": {
                    "composite": {
                        "size": 1000,
                        "sources": [
                            {"remote_addr": {"terms": {"field": "remote_addr"}}}
                        ]
                    },
                    "aggregations": {
                        "status": {"terms": {"field": "status"}},
                        "path": {"terms": {"field": "path"}},
                        "path_categories": {"terms": {"field": "path_type"}},
                        "request_length": {"extended_stats": {"field": "request_length"}},
                        "body_bytes_sent": {"extended_stats": {"field": "body_bytes_sent"}},
                        "request_time": {"extended_stats": {"field": "request_time"}},
                        "referer_categories": {
                            "filters": {
                                "filters": {
                                    "empty_referer": {"term": {"http_referer.keyword": "-"}},
                                    "non_empty_referer": {
                                        "bool": {"must_not": {"term": {"http_referer.keyword": "-"}}}
                                    }
                                }
                            }
                        },
                        "http_user_agent": {"terms": {"field": "http_user_agent.keyword"}}
                    }
                }
            }
        }
        buckets = []
        after_key = None
        while True:
            if after_key:
                query["aggregations"]["ip"]["composite"]["after"] = after_key

            res = self.get_client().search(index=index_name, body=query)
            page_buckets = res["aggregations"]["ip"]["buckets"]
            buckets.extend(page_buckets)

            after_key = res["aggregations"]["ip"].get("after_key")
            if not after_key:
                break
        return [self.parse_bucket_to_model(bucket, batch_id) for bucket in buckets]

    @staticmethod
    def parse_terms_buckets(buckets):
        """解析 terms 聚合成 List[KeyValue]"""
        return [
            KeyValue(key=str(bucket["key"]), value=bucket["doc_count"])
            for bucket in buckets
        ]

    @staticmethod
    def parse_extended_stats(stats):
        """解析 extended_stats 聚合成 ExtendedStats 模型"""
        if not stats:
            return None
        bounds = stats.get("std_deviation_bounds", {})
        return ExtendedStats(
            count=stats.get("count", 0),
            min=stats.get("min", 0.0),
            max=stats.get("max", 0.0),
            avg=stats.get("avg", 0.0),
            sum=stats.get("sum", 0.0),
            sum_of_squares=stats.get("sum_of_squares", 0.0),
            variance=stats.get("variance", 0.0),
            variance_population=stats.get("variance_population", 0.0),
            variance_sampling=stats.get("variance_sampling", 0.0),
            std_deviation=stats.get("std_deviation", 0.0),
            std_deviation_population=stats.get("std_deviation_population", 0.0),
            std_deviation_sampling=stats.get("std_deviation_sampling", 0.0),
            std_deviation_bounds=StdDeviationBound(
                upper=bounds.get("upper", 0.0),
                lower=bounds.get("lower", 0.0),
                upper_population=bounds.get("upper_population", 0.0),
                lower_population=bounds.get("lower_population", 0.0),
                upper_sampling=bounds.get("upper_sampling", 0.0),
                lower_sampling=bounds.get("lower_sampling", 0.0),
            )
        )

    def parse_bucket_to_model(self, bucket, batch_id: str) -> AccessIpAggregation:
        # referer_categories 是 filters 聚合
        referer_list = [
            KeyValue(key=key, value=value.get("doc_count", 0))
            for key, value in bucket.get("referer_categories", {}).get("buckets", {}).items()
        ]
        return AccessIpAggregation(
            ip=bucket["key"]["remote_addr"],
            count=bucket["doc_count"],
            status=self.parse_terms_buckets(bucket["status"]["buckets"]),
            path=self.parse_terms_buckets(bucket["path"]["buckets"]),
            path_categories=self.parse_terms_buckets(bucket["path_categories"]["buckets"]),
            request_length=self.parse_extended_stats(bucket["request_length"]),
            body_bytes_sent=self.parse_extended_stats(bucket["body_bytes_sent"]),
            request_time=self.parse_extended_stats(bucket["request_time"]),
            http_user_agent=self.parse_terms_buckets(bucket["http_user_agent"]["buckets"]),
            referer_categories=referer_list,
            batch_id=batch_id
        )
