from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from ..common.enums import CategoryEnum
from .enums import ArticleStatusEnum
from uuid import uuid4

class Article(BaseModel):
    """기사 컬렉션 모델"""

    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id", description="기사 ID")
    preview: Optional[str] = Field(default="", description="기사 프리뷰")
    title: str = Field(..., description="기사 제목")
    content: Optional[str] = Field(..., description="기사 본문 내용")
    summary: Optional[str] = Field(None, description="기사 요약")
    url: str = Field(..., description="기사 URL")
    reporter: Optional[str] = Field(None, description="기자 이름")
    published_at: datetime = Field(..., alias="publishedAt", description="발행 시간")
    issue_id: Optional[str] = Field(None, alias="issueId", description="관련 이슈 ID")
    category: CategoryEnum = Field(..., description="기사 카테고리")
    image_url: Optional[str] = Field(None, alias="imageUrl", description="기사 이미지 URL")
    source_id: str = Field(..., alias="sourceId", description="미디어 소스 ID")
    embedding: Optional[List[float]] = Field(None, description="기사 임베딩 벡터")
    status: Optional[ArticleStatusEnum] = Field(
        ArticleStatusEnum.PENDING, description="기사 처리 상태", alias="status"
    )

    model_config = {"populate_by_name": True}
