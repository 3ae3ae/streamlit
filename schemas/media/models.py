from pydantic import BaseModel, Field

from ..common.enums import PerspectiveEnum


class CategoryInfo(BaseModel):
    """미디어 소스의 카테고리 정보"""

    name: str = Field(...)
    url: str = Field(...)


