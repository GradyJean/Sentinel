from models.tag import IpTagRule
from storage.document import ElasticSearchRepository


class IpTagRuleManager(ElasticSearchRepository[IpTagRule]):
    """
    分数规则服务
    """

    def __init__(self):
        super().__init__("ip_tag_rule", IpTagRule)
