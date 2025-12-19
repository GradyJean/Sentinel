import ipaddress
from typing import List


def minimal_ip_segments(ips: List[str]) -> List[str]:
    networks = [
        ipaddress.ip_network(f"{ip}/32", strict=False)
        for ip in ips
    ]

    collapsed = ipaddress.collapse_addresses(networks)
    return [str(n) for n in collapsed]


if __name__ == '__main__':
    ips = [
        "66.249.64.163",
        "159.226.171.19",
        "180.153.236.52",
        "180.153.236.34",
        "180.153.236.62",
        "180.153.236.57",
        "180.153.236.43",
        "180.153.236.60",
        "180.153.236.36",
        "180.153.236.33",
        "180.153.236.32",
        "180.153.236.58",
        "180.153.236.47",
        "180.153.236.42",
        "180.153.236.37",
        "180.153.236.59",
        "180.153.236.44",
        "180.153.236.35",
        "180.153.236.49",
        "180.153.236.41"
    ]

cidr = minimal_ip_segments(ips)
print(cidr)