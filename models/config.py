from pydantic import BaseModel

"""
配置类
"""


class ServerConfig(BaseModel):
    """
    服务配置
    """
    host: str = "0.0.0.0"
    port: int = 8080
    base_path: str = ""
    static_path: str = ""


class NginxConfig(BaseModel):
    """
    Nginx 配置
    """
    base_path: str = ""
    log_path: str = ""
    conf_path: str = ""
    black_list_file: str = ""
    rate_limit_file: str = ""


class ElasticsearchConfig(BaseModel):
    """
    Elasticsearch 配置
    """
    url: str = ""
    username: str = ""
    password: str = ""
