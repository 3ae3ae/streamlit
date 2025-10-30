from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from ..common.enums import PerspectiveEnum
from .collections import UserPoliticalPreferenceDetailHistory
from .models import Period, UserPoliticalScoreHistoryWithoutMetadata


class DasiScoreResponse(BaseModel):
    """다시 스코어 조회 응답"""

    score: float = Field(..., description="현재 다시 스코어")
    user_id: str = Field(..., alias="userId", description="사용자 ID")

    model_config = {"populate_by_name": True}


class UserPoliticalScoreResponse(BaseModel):
    period: Period = Field(..., description="기간")
    score: Optional[UserPoliticalScoreHistoryWithoutMetadata] = Field(None, description="정치성향 점수")

    model_config = {"populate_by_name": True}


class UserPoliticalScoreListResponse(BaseModel):
    """사용자 정치성향 점수 히스토리 목록 응답"""

    history: List[UserPoliticalScoreResponse] = Field(
        default_factory=list, description="정치성향 점수 히스토리 목록"
    )

    model_config = {"populate_by_name": True}


class PoliticalPreferenceGetResponse(BaseModel):
    """정치성향 조회 응답"""

    nickname: str = Field("annonymous", description="사용자 닉네임")
    perspective: PerspectiveEnum


class PoliticalPreferenceDetailResponse(BaseModel):
    """사용자 상세 정치성향 응답"""

    politics: List[int] = Field(
        ...,
        min_length=3,
        max_length=3,
        description="정치 분야 성향 점수 [좌성향, 중도, 우성향]",
    )
    economy: List[int] = Field(
        ...,
        min_length=3,
        max_length=3,
        description="경제 분야 성향 점수 [좌성향, 중도, 우성향]",
    )
    society: List[int] = Field(
        ...,
        min_length=3,
        max_length=3,
        description="사회 분야 성향 점수 [좌성향, 중도, 우성향]",
    )
    culture: List[int] = Field(
        ...,
        min_length=3,
        max_length=3,
        description="생활/문화 분야 성향 점수 [좌성향, 중도, 우성향]",
    )
    technology: List[int] = Field(
        ...,
        min_length=3,
        max_length=3,
        description="IT/과학 분야 성향 점수 [좌성향, 중도, 우성향]",
    )
    international: List[int] = Field(
        ...,
        min_length=3,
        max_length=3,
        description="세계 분야 성향 점수 [좌성향, 중도, 우성향]",
    )
    overall: List[int] = Field(
        ...,
        min_length=3,
        max_length=3,
        description="전체 성향 점수 [좌성향, 중도, 우성향]",
    )


class PoliticalPreferenceDetailHistoryResponse(BaseModel):
    """사용자 정치성향 기록 응답"""

    has_more: bool = Field(..., alias="hasMore", description="추가 기록 여부")
    last_recorded_at: Optional[datetime] = Field(None, alias="lastRecordedAt", description="마지막 기록 시간")
    history: List[UserPoliticalPreferenceDetailHistory] = Field(
        ..., description="정치성향 기록 목록"
    )


class UserProfileResponse(BaseModel):
    """사용자 프로필 조회 응답"""

    nickname: str = Field("annonymous", description="사용자 닉네임")
    image_url: Optional[str] = Field(
        None, alias="imageUrl", description="프로필 이미지 presigned URL (없으면 null)"
    )
    political_preference: PerspectiveEnum = Field(
        PerspectiveEnum.center,
        alias="politicalPreference",
        description="사용자 정치성향",
    )

    model_config = {"populate_by_name": True}


class UserProfileItem(BaseModel):
    """여러 사용자 프로필 이미지 응답 항목"""

    user_id: str = Field(..., alias="userId")
    image_url: Optional[str] = Field(None, alias="imageUrl")

    model_config = {"populate_by_name": True}


class UserProfileBatchGetResponse(BaseModel):
    """여러 사용자 프로필 이미지 조회 응답"""

    profiles: List[UserProfileItem] = Field(default_factory=list)

    model_config = {"populate_by_name": True}


class ProfileUploadUrlResponse(BaseModel):
    """프로필 이미지 업로드 URL 응답"""

    upload_url: str = Field(..., alias="uploadUrl", description="업로드용 presigned PUT URL")
    upload_key: str = Field(..., alias="uploadKey", description="업로드 키 (commit시 사용)")
    expires_at: datetime = Field(..., alias="expiresAt", description="URL 만료 시간")

    model_config = {"populate_by_name": True}


class GlobalNotificationGetResponse(BaseModel):
    """전역 알림 설정 조회 응답"""

    comment_like_enabled: bool = Field(..., alias="commentLikeEnabled")
    comment_reply_enabled: bool = Field(..., alias="commentReplyEnabled")
    major_comment_enabled: bool = Field(..., alias="majorCommentEnabled")
    issue_subscription_enabled: bool = Field(..., alias="issueSubscriptionEnabled")
    media_subscription_enabled: bool = Field(..., alias="mediaSubscriptionEnabled")
    topic_subscription_enabled: bool = Field(..., alias="topicSubscriptionEnabled")

    model_config = {"populate_by_name": True}
