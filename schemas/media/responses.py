from typing import List, Optional

from pydantic import BaseModel, Field

from ..common.responses import ArticleListResponse
from ..common.enums import PerspectiveEnum
from ..common.models import SourceInfo
from ..common.responses import SourceInfoResponse

from uuid import uuid4

class MediaResponse(BaseModel):
    """매체 응답 모델"""

    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    name: str = Field(..., max_length=200, min_length=1)
    description: str = Field(default="", max_length=1000)
    perspective: PerspectiveEnum
    url: str = Field(default="", alias="url", max_length=2000)
    logo_url: str = Field(..., alias="logoUrl", max_length=2000)
    recent_articles: "ArticleListResponse" = Field(..., alias="recentArticles")
    is_subscribed: bool = Field(False, alias="isSubscribed")
    user_evaluated_perspective: Optional[PerspectiveEnum] = Field(
        None, alias="userEvaluatedPerspective"
    )

    model_config = {"populate_by_name": True}


class MediaDetailResponse(MediaResponse):
    """매체 상세 응답 모델"""

    ai_evaluated_perspective: Optional[str] = Field(None, alias="aiEvaluatedPerspective")
    expert_evaluated_perspective: Optional[str] = Field(
        None, alias="expertEvaluatedPerspective"
    )
    public_evaluated_perspective: Optional[str] = Field(
        None, alias="publicEvaluatedPerspective", ge=0, le=100
    )
    followers_count: int = Field(default=0, alias="followersCount", ge=0)
    user_evaluated_perspective: Optional[str] = Field(
        None, alias="userEvaluatedPerspective", description="사용자 평가 정치성향"
    )
    notification_enabled: bool = Field(default=False, alias="notificationEnabled")


class MediaListResponse(BaseModel):
    """매체 목록 응답 모델"""

    media: List[MediaResponse]
    has_more: bool = Field(..., alias="hasMore")
    last_media_id: Optional[str] = Field(None, alias="lastMediaId")

    model_config = {"populate_by_name": True}


class SourcesWithArticlesResponse(BaseModel):
    """소스 목록과 기사 목록을 포함하는 응답 모델"""

    sources: List[SourceInfoResponse] = Field(..., description="미디어 소스 목록")
    articles: ArticleListResponse = Field(..., description="기사 목록")

    model_config = {"populate_by_name": True}


class SourceInfoListResponse(BaseModel):
    """소스 정보 목록 응답 모델"""

    sources: List[SourceInfoResponse] = Field(..., description="소스 정보 목록")

    model_config = {"populate_by_name": True}


class SourceEvaluatedResponse(SourceInfoResponse):
    """언론사 평가 응답 모델"""

    user_evaluated_perspective: PerspectiveEnum = Field(
        None, alias="userEvaluatedPerspective", description="사용자 평가 정치성향"
    )


class SourceEvaluatedListResponse(BaseModel):
    """언론사 평가 목록 응답 모델"""

    sources: List[SourceEvaluatedResponse] = Field(default_factory=list, description="언론사 목록")
    has_more: bool = Field(..., alias="hasMore", description="추가 언론사 여부")
    last_source_id: Optional[str] = Field(None, alias="lastSourceId", description="마지막 언론사 ID")

    model_config = {"populate_by_name": True}
