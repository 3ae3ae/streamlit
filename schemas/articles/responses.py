from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from ..common.enums import CategoryEnum
from ..common.models import SourceInfo
from ..common.responses import ArticleListResponse, ArticleResponse
from uuid import uuid4
class SimilarityArticleResponse(BaseModel):
    """유사 기사 응답 모델"""

    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    title: str
    preview: str
    url: str
    reporter: Optional[str] = None
    published_at: datetime = Field(..., alias="publishedAt")
    issue_id: Optional[str] = Field(None, alias="issueId")
    category: CategoryEnum
    image_url: Optional[str] = Field(None, alias="imageUrl")
    source: SourceInfo
    similarity: float = Field(..., alias="similarity")
    model_config = {"populate_by_name": True}


class SimilarityArticleListResponse(BaseModel):
    """유사 기사 목록 응답 모델"""

    articles: List[SimilarityArticleResponse]
    has_more: bool = Field(..., alias="hasMore")
    last_article_id: str = Field(..., alias="lastArticleId")

    model_config = {"populate_by_name": True}
