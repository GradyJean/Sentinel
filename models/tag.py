from datetime import datetime
from typing import Optional

from models.storage.document import ElasticSearchModel


class IpTagRule(ElasticSearchModel):
    """
    标签规则
    """
    """
    评分规则
    """
    rule_name: str  # 规则名称
    condition: str  # 条件
    description: str  # 描述
    created_at: Optional[datetime] = None  # 创建时间
    updated_at: Optional[datetime] = None  # 更新时间
    enabled: bool = True  # 是否启用
