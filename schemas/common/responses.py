from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, Field

from .models import ErrorDetail, SourceInfo
from uuid import uuid4
from .enums import CategoryEnum


class ErrorResponse(BaseModel):
    """에러 응답 모델"""

    code: str
    message: str
    timestamp: str
    details: Optional[List[ErrorDetail]] = None


class SimpleSuccessResponse(BaseModel):
    """간단한 성공 응답"""

    message: str
    timestamp: datetime
    data: Optional[Any] = None

class SourceInfoResponse(SourceInfo):
    is_subscribed: bool = Field(False, alias="isSubscribed", description="사용자 구독 여부")

    model_config = {"populate_by_name": True}
    

class ArticleResponse(BaseModel):
    """기사 응답 모델"""

    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    title: str
    preview: Optional[str] = Field(default="", description="기사 프리뷰")
    url: str
    reporter: Optional[str] = None
    published_at: datetime = Field(..., alias="publishedAt")
    issue_id: Optional[str] = Field(None, alias="issueId")
    category: CategoryEnum
    image_url: Optional[str] = Field(None, alias="imageUrl")
    source: "SourceInfoResponse" = Field(..., description="기사 소스 정보")

    model_config = {"populate_by_name": True}    

class ArticleListResponse(BaseModel):
    """기사 목록 응답 모델"""

    articles: List[ArticleResponse]
    has_more: bool = Field(..., alias="hasMore")
    last_article_id: Optional[str] = Field(None, alias="lastArticleId")

    model_config = {"populate_by_name": True}