from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from ..articles.responses import ArticleListResponse
from ..comments.responses import CommentResponse
from ..common.enums import CategoryEnum, PerspectiveEnum
from ..media.responses import SourceInfoResponse
from .models import BackgroundKeywordRefs, CoverageSpectrum, Tag
from uuid import uuid4

class IssueResponse(BaseModel):
    """이슈 기본 응답 모델 (목록용)"""

    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    title: str
    category: CategoryEnum
    summary: str
    image_url: Optional[str] = Field(None, alias="imageUrl")
    image_source_name: Optional[str] = Field(None, alias="imageSourceName", description="이슈 이미지 출처명")
    image_source_url: Optional[str] = Field(None, alias="imageSourceUrl", description="이슈 이미지 출처 URL (기사 URL)")
    keywords: List[str] = Field(default_factory=list)
    published_at: Optional[datetime] = Field(
        None, alias="publishedAt", description="이슈 발행 시간 (없을 경우 createdAt 사용)"
    )
    created_at: datetime = Field(default_factory=datetime.now, alias="createdAt")
    view: int
    is_read: Optional[bool] = Field(None, alias="isRead", description="읽었는 지 여부")
    left_like_count: int = Field(default=0, alias="leftLikeCount", ge=0)
    center_like_count: int = Field(default=0, alias="centerLikeCount", ge=0)
    right_like_count: int = Field(default=0, alias="rightLikeCount", ge=0)
    coverage_spectrum: CoverageSpectrum = Field(..., alias="coverageSpectrum")
    sources: List[SourceInfoResponse] = Field(default_factory=list, description="관련 미디어 소스 목록")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt", description="업데이트 시간")
    is_subscribed: bool = Field(False, alias="isSubscribed", description="사용자 구독 여부")
    is_hot: Optional[bool] = Field(None, alias="isHot", description="핫 이슈 여부")
    hot_time: Optional[datetime] = Field(None, alias="hotTime", description="핫이슈로 지정된 시간")
    is_available: Optional[bool] = Field(None, alias="isAvailable", description="이슈 사용 가능 여부")
    tags: List[Tag] = Field(default_factory=list, alias="tags")
    comments_preview: Optional[List[CommentResponse]] = Field(
        None, alias="commentsPreview", description="이슈 인기 댓글 미리보기"
    )
    comments_count_preview: Optional[int] = Field(
        0, alias="commentsCountPreview", description="이슈 댓글 수 미리보기"
    )
    is_education: bool = Field(
        default=False,
        alias="isEducation",
        description="교육용 이슈 여부",
    )
    model_config = {"populate_by_name": True}


class IssueEvaluatedResponse(IssueResponse):
    user_evaluated_perspective: PerspectiveEnum = Field(
        None, alias="userEvaluatedPerspective", description="사용자 평가 정치성향"
    )


class IssueEvaluatedListResponse(BaseModel):
    """이슈 평가 응답 모델"""

    issues: List[IssueEvaluatedResponse] = Field(default_factory=list, description="이슈 목록")
    has_more: bool = Field(..., alias="hasMore", description="추가 이슈 여부")
    last_issue_id: Optional[str] = Field(None, alias="lastIssueId", description="마지막 이슈 ID")

    model_config = {"populate_by_name": True}


class IssueDetailResponse(IssueResponse):
    """이슈 상세 응답 모델 - IssueResponse를 상속"""
    comments_count: int = Field(..., alias="commentsCount", description="이슈 댓글 수")
    left_summary: str = Field(..., alias="leftSummary")
    center_summary: str = Field(..., alias="centerSummary")
    right_summary: str = Field(..., alias="rightSummary")
    common_summary: Optional[str] = Field(None, alias="commonSummary")
    user_evaluation: Optional[PerspectiveEnum] = Field(
        None, alias="userEvaluation", description="사용자 평가 정치성향"
    )
    bias_comparison: Optional[str] = Field(None, alias="biasComparison")
    left_comparison: Optional[str] = Field(None, alias="leftComparison")
    center_comparison: Optional[str] = Field(None, alias="centerComparison")
    right_comparison: Optional[str] = Field(None, alias="rightComparison")
    next_issues: Optional[List["IssueResponse"]] = Field(
        None,
        alias="nextIssues",
        description="다음 이슈 상세(이슈 응답 모델 재사용)",
    )
    next_issue_ids: Optional[List[str]] = Field(
        None,
        alias="nextIssueIds",
        description="다음 이슈 ID 목록",
    )
    left_keywords: Optional[List[str]] = Field(None, alias="leftKeywords")
    center_keywords: Optional[List[str]] = Field(None, alias="centerKeywords")
    right_keywords: Optional[List[str]] = Field(None, alias="rightKeywords")
    articles: "ArticleListResponse" = Field(..., alias="articles", description="이슈에 관련된 기사 목록")
    has_conflict: Optional[bool] = Field(None, alias="hasConflict")

    # 배경지식 키워드 참조 (isEducation=True일 때만 포함)
    background_keyword_refs: Optional["BackgroundKeywordRefs"] = Field(
        None,
        alias="backgroundKeywordRefs",
        description="배경지식 키워드 참조 목록 (클라이언트가 키워드 ID로 상세 조회 필요)",
    )


class IssueListResponse(BaseModel):
    """이슈 목록 응답 모델"""

    issues: List[IssueResponse]
    has_more: bool = Field(..., alias="hasMore")
    last_issue_id: Optional[str] = Field(None, alias="lastIssueId")

    model_config = {"populate_by_name": True}


class HotIssueListResponse(IssueListResponse):
    """핫 이슈 목록 응답 모델"""

    hot_time: datetime = Field(
        default_factory=datetime.now,
        alias="hotTime",
        description="핫이슈로 지정된 시간",
    )

    model_config = {"populate_by_name": True}


class IssueDetailFullResponse(BaseModel):
    """이슈 상세 전체 응답 모델"""

    issue: IssueDetailResponse
    articles: "ArticleListResponse"

    model_config = {"populate_by_name": True}


class CategoryIssuesListResponse(IssueListResponse):
    """카테고리 이슈 목록 응답 (IssueListResponse + category)"""

    category: CategoryEnum = Field(..., description="카테고리명")

    model_config = {"populate_by_name": True}


class CategorizedIssuesResponse(BaseModel):
    """카테고리별 이슈 리스트 집합"""

    categories: List[CategoryIssuesListResponse] = Field(
        default_factory=list, description="카테고리별 이슈 리스트"
    )

    model_config = {"populate_by_name": True}
