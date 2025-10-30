from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from ..common.enums import CategoryEnum
from .enums import IssueStatusEnum
from .models import BackgroundKeywordRefs, ClusterMetadata, CoverageSpectrum, Tag, ImagesByPerspective
from ..media import SourceInfo

from uuid import uuid4
class Issue(BaseModel):
    """이슈 컬렉션 모델"""

    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id", description="이슈 ID")
    title: str = Field(..., description="이슈 제목")
    category: CategoryEnum = Field(CategoryEnum.politics, description="이슈 카테고리")
    summary: Optional[str] = Field(None, description="이슈 요약")
    image_url: Optional[str] = Field(None, alias="imageUrl", description="이슈 관련 이미지 URL")
    image_source: Optional[str] = Field(None, alias="imageSource", description="이슈 이미지 출처")
    is_hot: bool = Field(default=False, alias="isHot", description="핫이슈 여부")
    hot_time: Optional[datetime] = Field(None, alias="hotTime", description="핫이슈로 지정된 시간")
    is_available: bool = Field(default=False, alias="isAvailable", description="이슈 사용 가능 여부")
    keywords: Optional[List[str]] = Field(default_factory=list, description="이슈 관련 키워드")
    created_at: datetime = Field(..., alias="createdAt", description="생성 시간")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt", description="업데이트 시간")
    left_like_count: int = Field(default=0, ge=0, alias="leftLikeCount", description="좌성향 좋아요 수")
    center_like_count: int = Field(default=0, ge=0, alias="centerLikeCount", description="중도 좋아요 수")
    right_like_count: int = Field(default=0, ge=0, alias="rightLikeCount", description="우성향 좋아요 수")
    common_summary: Optional[str] = Field(None, alias="commonSummary", description="공통 요약")
    center_summary: Optional[str] = Field(None, alias="centerSummary", description="중도 관점 요약")
    right_summary: Optional[str] = Field(None, alias="rightSummary", description="우성향 관점 요약")
    left_summary: Optional[str] = Field(None, alias="leftSummary", description="좌성향 관점 요약")
    bias_comparison: Optional[str] = Field(None, alias="biasComparison", description="편향 비교 요약")
    pulished_at: Optional[datetime] = Field(None, alias="publishedAt", description="이슈가 공개된 시간")
    left_comparison: Optional[str] = Field(
        None,
        alias="leftComparison",
        description="진보 성향 언론사의 보도 특징과 차이점",
    )
    center_comparison: Optional[str] = Field(
        None,
        alias="centerComparison",
        description="중도 성향 언론사의 보도 특징과 차이점",
    )
    right_comparison: Optional[str] = Field(
        None,
        alias="rightComparison",
        description="보수 성향 언론사의 보도 특징과 차이점",
    )
    view: int = Field(default=0, ge=0, description="조회 수")
    left_keywords: Optional[List[str]] = Field(
        default_factory=list, alias="leftKeywords", description="좌성향 키워드"
    )
    center_keywords: Optional[List[str]] = Field(
        default_factory=list, alias="centerKeywords", description="중도 키워드"
    )
    right_keywords: Optional[List[str]] = Field(
        default_factory=list, alias="rightKeywords", description="우성향 키워드"
    )
    coverage_spectrum: Optional[CoverageSpectrum] = Field(
        None, alias="coverageSpectrum", description="정치적 스펙트럼 분포"
    )
    sources: List["SourceInfo"] = Field(
        default_factory=list, description="이슈에 관련된 미디어 소스 목록"
    )
    tags: Optional[List[Tag]] = Field(default_factory=list, description="이슈 태그 목록")
    has_conflict: bool = Field(default=False, alias="hasConflict", description="대립 여부")
    cluster_metadata: Optional[ClusterMetadata] = Field(
        None, alias="clusterMetadata", description="이슈 클러스터링 메타데이터"
    )
    review_reason: Optional[str] = Field(None, alias="reviewReason", description="콘텐츠 생성 검토가 필요한 이유")
    status: Optional[IssueStatusEnum] = Field(
        default=IssueStatusEnum.PENDING_INFO_GENERATION.value, 
        description="이슈 처리 상태"
    )
    images_by_perspective: Optional[ImagesByPerspective] = Field(
        None,
        alias="imagesByPerspective",
        description="성향별(좌/중도/우) 기사 이미지 후보 목록",
    )
    background_keyword_refs: Optional[BackgroundKeywordRefs] = Field(
        None,
        alias="backgroundKeywordRefs",
        description="배경지식 키워드 참조 목록",
    )
    is_education: bool = Field(
        default=False,
        alias="isEducation",
        description="교육용 이슈 여부 (True일 때만 배경지식 키워드 표시)",
    )

    model_config = {"populate_by_name": True}


class UserIssueEvaluation(BaseModel):
    """사용자 이슈 평가 컬렉션 모델"""

    user_id: str = Field(..., alias="userId", description="사용자 이메일")
    issue_id: str = Field(..., alias="issueId", description="이슈 ID")
    perspective: str = Field(..., pattern="^(left|center|right)$", description="평가한 성향")
    evaluated_at: datetime = Field(default_factory=datetime.now, alias="evaluatedAt", description="평가 시간")

    model_config = {"populate_by_name": True}
