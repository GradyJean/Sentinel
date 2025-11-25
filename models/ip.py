import ipaddress

from pydantic import BaseModel
from typing import Optional, List, Self


class IpSegments(BaseModel):
    org_name: Optional[str] = None  # 机构名称
    is_internal: Optional[bool] = None  # 是否内网
    start_ip: str  # 起始 IP
    end_ip: str  # 结束 IP
    cidr: Optional[str] = None  # CIDR 格式（可选）
    tags: Optional[List[str]] = None  # 标签列表

    def auto_fill_cidr(self) -> Self:
        if not self.cidr:
            networks = ipaddress.summarize_address_range(
                ipaddress.ip_address(self.start_ip),
                ipaddress.ip_address(self.end_ip)
            )
            self.cidr = str(list(networks)[0])
        return self
