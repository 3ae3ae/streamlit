from typing import List, Optional

from pydantic import BaseModel, Field

from ..common.enums import CategoryEnum, PerspectiveEnum
from ..issues.models import Tag
from ..topics.enums import TopicStatusEnum


class AdminFcmSendRequest(BaseModel):
    """관리자 FCM 전송 요청 모델"""

    title: str = Field(description="알림 제목")
    body: str = Field(description="알림 본문")
    type: Optional[str] = Field("Send", description="알림 타입")
    image: Optional[str] = Field(None, description="알림 이미지 URL")
    data: Optional[dict[str, str]] = Field(None, description="데이터 페이로드(문자열 키/값)")
    topic: Optional[str] = Field(None, description="전송할 토픽 이름(없으면 기본 allUserTopic)")
    tokens: Optional[List[str]] = Field(None, description="전송 대상 디바이스 토큰 목록")

    model_config = {"populate_by_name": True}


class IssueCreateRequest(BaseModel):
    """이슈 생성 요청 모델"""

    title: str = Field(..., description="이슈 제목")
    category: CategoryEnum = Field(..., description="이슈 카테고리")
    summary: Optional[str] = Field(None, description="이슈 요약")
    image_url: Optional[str] = Field(None, alias="imageUrl", description="이슈 이미지 URL")
    image_source: Optional[str] = Field(None, alias="imageSource", description="이슈 이미지 출처")
    is_hot: bool = Field(default=False, alias="isHot", description="핫이슈 여부")
    is_available: bool = Field(default=True, alias="isAvailable", description="이슈 사용 가능 여부")
    keywords: Optional[List[str]] = Field(default_factory=list, description="이슈 키워드")

    model_config = {"populate_by_name": True}


class IssueUpdateRequest(BaseModel):
    """이슈 수정 요청 모델"""

    title: Optional[str] = Field(None, description="이슈 제목")
    category: Optional[CategoryEnum] = Field(None, description="이슈 카테고리")
    summary: Optional[str] = Field(None, description="이슈 요약")
    left_summary: Optional[str] = Field(None, alias="leftSummary", description="좌성향 관점 요약")
    center_summary: Optional[str] = Field(None, alias="centerSummary", description="중도 관점 요약")
    right_summary: Optional[str] = Field(None, alias="rightSummary", description="우성향 관점 요약")
    common_summary: Optional[str] = Field(None, alias="commonSummary", description="공통 요약")
    bias_comparison: Optional[str] = Field(None, alias="biasComparison", description="편향 비교 요약")
    left_comparison: Optional[str] = Field(None, alias="leftComparison", description="좌성향 비교")
    center_comparison: Optional[str] = Field(None, alias="centerComparison", description="중도 비교")
    right_comparison: Optional[str] = Field(None, alias="rightComparison", description="우성향 비교")
    image_url: Optional[str] = Field(None, alias="imageUrl", description="이슈 이미지 URL")
    image_source: Optional[str] = Field(None, alias="imageSource", description="이슈 이미지 출처")
    is_hot: Optional[bool] = Field(None, alias="isHot", description="핫이슈 여부")
    is_available: Optional[bool] = Field(None, alias="isAvailable", description="이슈 사용 가능 여부")
    keywords: Optional[List[str]] = Field(None, description="이슈 키워드")
    left_keywords: Optional[List[str]] = Field(None, alias="leftKeywords", description="좌성향 키워드")
    center_keywords: Optional[List[str]] = Field(None, alias="centerKeywords", description="중도 키워드")
    right_keywords: Optional[List[str]] = Field(None, alias="rightKeywords", description="우성향 키워드")
    tags: Optional[List[Tag]] = Field(None, description="이슈 태그 목록")
    has_conflict: Optional[bool] = Field(None, alias="hasConflict", description="대립 여부")

    model_config = {"populate_by_name": True}


class IssueAddArticlesRequest(BaseModel):
    """이슈에 기사 추가 요청 모델"""

    article_id_list: List[str] = Field(
        ...,
        alias="articleIdList",
        min_length=1,
        description="이슈에 추가할 기사 ID 목록",
    )
    model_config = {"populate_by_name": True}


class IssueCombineRequest(BaseModel):
    """이슈 결합 요청 모델"""

    first_issue_id: str = Field(..., alias="firstIssueId", description="첫 번째 이슈 ID")
    second_issue_id: str = Field(..., alias="secondIssueId", description="두 번째 이슈 ID")


class TopicCreateRequest(BaseModel):
    """토픽 생성 요청 모델"""

    name: str = Field(..., description="토픽 이름")
    category: CategoryEnum = Field(..., description="토픽이 속한 카테고리")

    model_config = {"populate_by_name": True}


class TopicUpdateRequest(BaseModel):
    """토픽 수정 요청 모델"""

    name: Optional[str] = Field(None, description="토픽 이름")
    category: Optional[CategoryEnum] = Field(None, description="토픽이 속한 카테고리")
    status: Optional[TopicStatusEnum] = Field(None, description="토픽 상태")

    model_config = {"populate_by_name": True}


class AdminArticleRequestQueryParams(BaseModel):
    """관리자 기사 요청 쿼리 파라미터 검증 모델"""

    limit: Optional[int] = Field(
        default=10, ge=1, le=50, description="한 번에 가져올 항목 수"
    )
    last_article_id: Optional[str] = Field(
        None, alias="lastArticleId", description="마지막 기사 ID (페이징용)"
    )
    issue_id: Optional[str] = Field(None, alias="issueId", description="특정 이슈 ID로 필터링")
    source_id: Optional[str] = Field(None, alias="sourceId", description="특정 미디어 소스 ID로 필터링")
    perspective: Optional[PerspectiveEnum] = Field(None, description="정치적 성향으로 필터링")
    category: Optional[CategoryEnum] = Field(None, description="카테고리로 필터링")

    model_config = {"populate_by_name": True}


class NoticeCreateRequest(BaseModel):
    """공지사항 생성 요청 모델"""

    title: str = Field(..., description="공지사항 제목")
    content: Optional[str] = Field(None, description="공지사항 내용 (isImage가 True면 선택사항)")
    url: str = Field(..., description="공지사항 URL")
    is_image: bool = Field(..., alias="isImage", description="이미지 여부")
    is_important: Optional[bool] = Field(
        default=False, alias="isImportant", description="중요 공지 여부"
    )

    model_config = {"populate_by_name": True}


class NoticeUpdateRequest(BaseModel):
    """공지사항 수정 요청 모델"""

    title: Optional[str] = Field(None, description="공지사항 제목")
    content: Optional[str] = Field(None, description="공지사항 내용")
    url: Optional[str] = Field(None, description="공지사항 URL")
    is_image: Optional[bool] = Field(None, alias="isImage", description="이미지 여부")
    is_important: Optional[bool] = Field(
        None, alias="isImportant", description="중요 공지 여부"
    )
    is_active: Optional[bool] = Field(None, alias="isActive", description="활성화 여부")

    model_config = {"populate_by_name": True}


class AdminPushMessageRequest(BaseModel):
    """푸시 메시지 생성 요청 (관리자용)

    - push message generator Lambda에 그대로 전달되는 스키마
    """

    issue_id: str = Field(..., alias="issueId", description="이슈 ID")
