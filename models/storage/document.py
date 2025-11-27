from typing import Optional

from pydantic import BaseModel, Field


class ElasticSearchModel(BaseModel):
    """
    ElasticsearchModel 用于查询 ES 库继承
    """
    id: Optional[str] = Field(default=None, exclude=True)