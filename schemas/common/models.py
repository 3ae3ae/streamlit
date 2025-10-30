from typing import Any, Optional

from pydantic import BaseModel, Field
from .enums import PerspectiveEnum

from uuid import uuid4
class ErrorDetail(BaseModel):
    """에러 상세 정보"""

    field: Optional[str] = None
    message: str
    value: Optional[Any] = None
    
class SourceInfo(BaseModel):
    """기사 응답에 포함될 소스 정보"""

    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    name: str
    perspective: PerspectiveEnum
    logo_url: str = Field(..., alias="logoUrl", description="로고 URL")

    model_config = {"populate_by_name": True}
