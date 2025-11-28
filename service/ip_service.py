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


class IpPolicyService(ElasticSearchRepository[IpPolicy]):
    """
    IP策略服务
    """

    def __init__(self):
        super().__init__("ip_policy", IpPolicy)
