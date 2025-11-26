from typing import Optional


class AppException(Exception):
    """应用基础异常类"""

    def __init__(self, message: str, code: int = 500, detail: Optional[str] = None):
        self.message = message
        self.code = code
        self.detail = detail


class ElasticsearchQueryError(AppException):
    """Elasticsearch查询异常"""

    def __init__(self, message: str, query: Optional[dict] = None):
        super().__init__(message, 500, str(query) if query else None)
        self.query = query


class InvalidKeywordError(AppException):
    """无效关键词异常"""

    def __init__(self, message: str):
        super().__init__(message, 400)
