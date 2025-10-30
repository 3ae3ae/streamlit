"""다음 이슈 추천 컬렉션 스키마.

하이브리드 추천 결과를 저장하며 CF/콘텐츠 기반 목록을 별도로 유지합니다.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from shared.schemas.issues.collections import Issue

class NextRecommendationItem(BaseModel):
    """다음 이슈 추천 아이템(뷰용)"""

    issue_id: str = Field(..., alias="issueId", description="추천 이슈 ID")
    issue: Issue = Field(..., alias="issue", description="추천 이슈 전체 스냅샷")
    score: Optional[float] = Field(None, alias="score", description="추천 점수 (협업/콘텐츠 기반)")
    origin: Optional[str] = Field(None, alias="origin", description="추천 생성 출처(cf/content)")

    model_config = {"populate_by_name": True}


class NextRecommendations(BaseModel):
    """기준 이슈별 다음 추천 이슈 목록(저장용)"""

    issue_id: str = Field(..., alias="issueId", description="기준 이슈 ID")
    cf_items: List[NextRecommendationItem] = Field(default_factory=list, alias="cfItems", description="협업 필터링 추천 목록")
    content_items: List[NextRecommendationItem] = Field(
        default_factory=list,
        alias="contentItems",
        description="콘텐츠 기반 추천 목록",
    )
    updated_at: datetime = Field(default_factory=datetime.utcnow, alias="updatedAt", description="업데이트 시각")

    model_config = {"populate_by_name": True}
