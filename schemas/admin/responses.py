from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from ..common.enums import CategoryEnum
from ..issues.models import ClusterMetadataAdmin, CoverageSpectrum, Tag, ImagesByPerspective
from ..issues.enums import IssueStatusEnum
from ..media.responses import SourceInfoResponse
from ..articles.responses import ArticleListResponse
from uuid import uuid4
from ..comments.responses import MajorCommentItem
from ..users.enums import UserEntitlementEnum


class AdminFcmSendResponse(BaseModel):
    """관리자 FCM 전송 응답 모델(토픽/토큰 공용)"""

    success: bool = Field(True, description="성공 여부")
    # 토픽 전송 결과
    message_id: Optional[str] = Field(None, description="전송된 메시지 ID")
    topic: Optional[str] = Field(None, description="전송된 토픽 명")
    # 토큰 전송 결과
    method: Optional[str] = Field(None, description="전송 방식 (send_each_for_multicast)")
    success_count: Optional[int] = Field(None, description="성공한 토큰 수")
    failure_count: Optional[int] = Field(None, description="실패한 토큰 수")
    message_ids: Optional[List[str]] = Field(None, description="성공 메시지 ID 목록")
    failed_tokens: Optional[List[dict]] = Field(None, description="실패한 토큰과 오류 목록")
    tokens_count: Optional[int] = Field(None, description="전송 대상 토큰 총 수")
    # 에러
    error: Optional[str] = Field(None, description="에러 메시지")

    model_config = {"populate_by_name": True}


class IssueAdminResponse(BaseModel):
    """이슈 관리자 응답 모델 (목록용) - cluster_metadata 포함"""

    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    title: str
    category: CategoryEnum
    summary: str
    image_source_name: Optional[str] = Field(None, alias="imageSourceName", description="이슈 이미지 출처명")
    image_source_url: Optional[str] = Field(None, alias="imageSourceUrl", description="이슈 이미지 출처 URL (기사 URL)")
    images_by_perspective: Optional[ImagesByPerspective] = Field(
        None, alias="imagesByPerspective", description="성향별(좌/중도/우) 이미지 후보 전체"
    )
    keywords: List[str] = Field(default_factory=list)
    created_at: datetime = Field(..., alias="createdAt")
    view: int
    left_like_count: int = Field(default=0, alias="leftLikeCount", ge=0)
    center_like_count: int = Field(default=0, alias="centerLikeCount", ge=0)
    right_like_count: int = Field(default=0, alias="rightLikeCount", ge=0)
    coverage_spectrum: CoverageSpectrum = Field(..., alias="coverageSpectrum")
    sources: List[SourceInfoResponse] = Field(default_factory=list, description="관련 미디어 소스 목록")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt", description="업데이트 시간")
    is_hot: Optional[bool] = Field(None, alias="isHot", description="핫 이슈 여부")
    hot_time: Optional[datetime] = Field(None, alias="hotTime", description="핫이슈로 지정된 시간")
    is_available: Optional[bool] = Field(None, alias="isAvailable", description="이슈 사용 가능 여부")
    reviews_count: Optional[int] = Field(None, alias="reviewCounts", description="검토 횟수")
    tags: List[Tag] = Field(default_factory=list, alias="tags")
    status: Optional[IssueStatusEnum] = Field(None, alias="status", description="이슈 상태")
    cluster_metadata: Optional[ClusterMetadataAdmin] = Field(
        None, alias="clusterMetadata", description="이슈 클러스터링 메타데이터"
    )

    model_config = {"populate_by_name": True}


class IssueDetailAdminResponse(IssueAdminResponse):
    """이슈 관리자 상세 응답 모델"""

    left_summary: Optional[str] = Field(None, alias="leftSummary")
    center_summary: Optional[str] = Field(None, alias="centerSummary")
    right_summary: Optional[str] = Field(None, alias="rightSummary")
    common_summary: Optional[str] = Field(None, alias="commonSummary")
    bias_comparison: Optional[str] = Field(None, alias="biasComparison")
    left_comparison: Optional[str] = Field(None, alias="leftComparison")
    center_comparison: Optional[str] = Field(None, alias="centerComparison")
    right_comparison: Optional[str] = Field(None, alias="rightComparison")
    next_issue_ids: Optional[List[str]] = Field(None, alias="nextIssueIds", description="다음 이슈 ID")
    left_keywords: Optional[List[str]] = Field(None, alias="leftKeywords")
    center_keywords: Optional[List[str]] = Field(None, alias="centerKeywords")
    right_keywords: Optional[List[str]] = Field(None, alias="rightKeywords")
    articles: "ArticleListResponse" = Field(..., alias="articles", description="이슈에 관련된 기사 목록")
    review_reason: Optional[str] = Field(None, alias="reviewReason")
    has_conflict: Optional[bool] = Field(None, alias="hasConflict")


class IssueListAdminResponse(BaseModel):
    """이슈 목록 응답 모델"""

    issues: List[IssueAdminResponse]
    has_more: bool = Field(..., alias="hasMore")
    last_issue_id: Optional[str] = Field(None, alias="lastIssueId")  # 마지막 페이지에서는 null일 수 있음

    model_config = {"populate_by_name": True}


class AdminPushMessageResponse(BaseModel):
    """푸시 메시지 생성 응답 (관리자용)

    - push message generator Lambda의 결과를 그대로 매핑
    """

    success: bool = Field(True, description="성공 여부")
    title: Optional[str] = Field(None, description="푸시 타이틀")
    body: Optional[str] = Field(None, description="푸시 본문")
    error: Optional[str] = Field(None, description="에러 메시지")


class AdminFcmLogItem(BaseModel):
    """FCM 메세징 로그 항목"""

    id: str = Field(..., description="로그 ID")
    type: str = Field(..., description="요청 타입: Send|Subscribe|Unsubscribe")
    success: bool = Field(..., description="성공 여부")
    topic: Optional[str] = Field(None, description="대상 토픽")
    tokens_count: Optional[int] = Field(None, alias="tokensCount", description="토큰 개수")
    admin_id: Optional[str] = Field(None, alias="adminId", description="요청한 관리자 ID")
    created_at: datetime = Field(..., alias="createdAt", description="생성 시각")
    request_payload: Optional[dict] = Field(None, alias="requestPayload", description="요청 페이로드")
    response: Optional[dict] = Field(None, description="응답 원문")

    model_config = {"populate_by_name": True}


class AdminFcmLogListResponse(BaseModel):
    """FCM 메세징 로그 목록 응답"""

    logs: list[AdminFcmLogItem] = Field(default_factory=list)
    has_more: bool = Field(False, alias="hasMore")
    last_log_id: Optional[str] = Field(None, alias="lastLogId")

    model_config = {"populate_by_name": True}


class AdminRecentMajorCommentListResponse(BaseModel):
    """어드민 최근 메이저 댓글 목록 (최신순, 페이지네이션)"""

    comments: List[MajorCommentItem] = Field(default_factory=list)
    has_more: bool = Field(False, alias="hasMore", description="다음 페이지 여부")
    last_comment_id: Optional[str] = Field(None, alias="lastCommentId", description="페이징용 마지막 댓글 ID")

    model_config = {"populate_by_name": True}


class AdminCommentItem(BaseModel):
    """어드민용 댓글 응답 모델 (perspective 정보 포함)"""

    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id", description="댓글 ID")
    content: str = Field(..., description="댓글 내용")
    created_at: datetime = Field(..., alias="createdAt", description="생성 시간")
    like_count: int = Field(0, alias="likeCount", ge=0, description="좋아요 수")
    is_deleted: bool = Field(False, alias="isDeleted", description="삭제 여부")
    source: Optional[List[str]] = Field(None, description="댓글 출처 url")
    nickname: str = Field(..., description="댓글 작성자 닉네임")
    image_url: Optional[str] = Field(None, alias="imageUrl", description="댓글 작성자 프로필 이미지 URL")
    is_liked: bool = Field(False, alias="isLiked", description="현재 사용자의 좋아요 여부")
    is_reported: bool = Field(False, alias="isReported", description="현재 사용자가 신고한 댓글 여부")
    perspective: str = Field(..., description="댓글 성향 (left|center|right)")
    issue_id: Optional[str] = Field(None, alias="issueId", description="이슈 ID")
    parent_comment_id: Optional[str] = Field(None, alias="parentCommentId", description="부모 댓글 ID")
    user_id: Optional[str] = Field(None, alias="userId", description="작성자 ID")
    entitlement: Optional[UserEntitlementEnum] = Field(
        UserEntitlementEnum.free,
        description="댓글 작성자의 유료 구독 등급",
    )
    replies: List["AdminCommentItem"] = Field(default_factory=list, description="답글 목록")

    model_config = {"populate_by_name": True}


class AdminCommentListResponse(BaseModel):
    """어드민용 댓글 목록 응답 (모든 성향 포함)"""

    comments: List[AdminCommentItem] = Field(default_factory=list, description="모든 성향의 댓글 목록")
    has_more: bool = Field(False, alias="hasMore", description="다음 페이지 여부")
    last_comment_id: Optional[str] = Field(None, alias="lastCommentId", description="페이징용 마지막 댓글 ID")
    total_count: Optional[int] = Field(None, alias="totalCount", description="전체 댓글 수")

    model_config = {"populate_by_name": True}


class AdminRecentCommentListResponse(BaseModel):
    """어드민 최근 댓글 목록"""

    comments: List[AdminCommentItem] = Field(default_factory=list)
    has_more: bool = Field(False, alias="hasMore", description="다음 페이지 여부")
    last_comment_id: Optional[str] = Field(None, alias="lastCommentId", description="페이징용 마지막 댓글 ID")

    model_config = {"populate_by_name": True}

class AdminDailyIssueStatsResponse(BaseModel):
    """어드민 일간 이슈 통계 응답 모델

    - 특정 날짜(KST)의 기준 충족 이슈, 시도, 실패/성공 건수
    - 그래프용 시간대별 집계(optional)
    """

    date: str = Field(..., description="요청 일자(YYYY-MM-DD, KST)")
    timezone: str = Field("KST", description="시간대 표기")
    threshold: int = Field(..., description="기준 멀티 소스 수")

    scheduled_count: int = Field(..., alias="scheduledCount", description="기준 충족 이슈 수")
    posted_count: int = Field(..., alias="postedCount", description="게시 완료 이슈 수")

    info_triggered_count: int = Field(0, alias="infoTriggeredCount")
    info_success_count: int = Field(0, alias="infoSuccessCount")
    info_failed_count: int = Field(0, alias="infoFailedCount")

    image_triggered_count: int = Field(0, alias="imageTriggeredCount")
    image_completed_count: int = Field(0, alias="imageCompletedCount")
    image_failed_count: int = Field(0, alias="imageFailedCount")

    model_config = {"populate_by_name": True}


class AdminDailyIssueDailyItem(BaseModel):
    """일별 통계 아이템 (그래프용)"""

    date: str = Field(..., description="일자(YYYY-MM-DD, KST)")
    scheduled_count: int = Field(..., alias="scheduledCount")
    posted_count: int = Field(..., alias="postedCount")

    info_triggered_count: int = Field(0, alias="infoTriggeredCount")
    info_success_count: int = Field(0, alias="infoSuccessCount")
    info_failed_count: int = Field(0, alias="infoFailedCount")

    image_triggered_count: int = Field(0, alias="imageTriggeredCount")
    image_completed_count: int = Field(0, alias="imageCompletedCount")
    image_failed_count: int = Field(0, alias="imageFailedCount")

    model_config = {"populate_by_name": True}


class AdminDailyIssueSeriesResponse(BaseModel):
    """기간별 일간 이슈 통계 응답 (그래프용)"""

    start_date: str = Field(..., alias="startDate", description="시작일(YYYY-MM-DD, KST)")
    end_date: str = Field(..., alias="endDate", description="종료일(YYYY-MM-DD, KST)")
    timezone: str = Field("KST", description="시간대 표기")
    threshold: int = Field(..., description="기준 멀티 소스 수")
    items: list[AdminDailyIssueDailyItem] = Field(default_factory=list)

    model_config = {"populate_by_name": True}
