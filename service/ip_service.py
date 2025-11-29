from typing import List, Dict

from loguru import logger

from models.ip import IpRecord, AllowedIpSegment, IpPolicy
from storage.document import ElasticSearchRepository


class IpRecordService(ElasticSearchRepository[IpRecord]):
    """
    IP记录服务
    """

    def __init__(self):
        super().__init__("ip_record", IpRecord)


class AllowedIpSegmentService(ElasticSearchRepository[AllowedIpSegment]):
    """
    允许的 IP 段服务
    """

    def __init__(self):
        super().__init__("allowed_ip_segment", AllowedIpSegment)

    def query_ip(self, ip: str) -> List[AllowedIpSegment]:
        query_body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "start_ip": {
                                    "lte": ip
                                }
                            }
                        },
                        {
                            "range": {
                                "end_ip": {
                                    "gte": ip
                                }
                            }
                        }
                    ]
                }
            }
        }
        return self.query_list(query_body)

    def query_ips(self, ips: List[str]) -> Dict[str, List[AllowedIpSegment]]:
        body = []
        for ip in ips:
            body.append({"index": self.index})
            body.append({
                "query": {
                    "bool": {
                        "must": [
                            {"range": {"start_ip": {"lte": ip}}},
                            {"range": {"end_ip": {"gte": ip}}}
                        ]
                    }
                }
            })

        results = self.get_client().msearch(body=body)
        # 解析返回值
        output: Dict[str, List[AllowedIpSegment]] = {}
        responses = results.get("responses", [])

        for i, res in enumerate(responses):
            ip = ips[i]
            hits = res.get("hits", {}).get("hits", [])
            segments = []
            for hit in hits:
                src = hit.get("_source", {})
                try:
                    segment = AllowedIpSegment(**src)
                except Exception as e:
                    logger.error(f"Failed to parse AllowedIpSegment for IP {ip}: {e}")
                    continue
                segments.append(segment)
            output[ip] = segments
        return output


class IpPolicyService(ElasticSearchRepository[IpPolicy]):
    """
    IP策略服务
    """

    def __init__(self):
        super().__init__("ip_policy", IpPolicy)
