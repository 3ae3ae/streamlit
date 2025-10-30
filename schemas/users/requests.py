from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from ..common.enums import PerspectiveEnum
from .enums import UserEntitlementEnum
from .models import UserPoliticalScoreHistoryWithoutMetadata


class WatchedArticleListRequest(BaseModel):
    article_ids: List[str] = Field(
        ...,
        min_length=1,
        description="시청한 기사 ID 목록",
        alias="articleIds"
    )

    model_config = {"populate_by_name": True}


class DasiScoreAddRequest(BaseModel):
    score: float = Field(..., ge=0.0, description="추가할 다시 스코어", example=10.0)

    model_config = {"populate_by_name": True}


class UserNicknameRequest(BaseModel):
    nickname: str = Field(..., min_length=1, max_length=20)

    model_config = {"populate_by_name": True}


class PoliticalPreferenceRequest(BaseModel):
    """정치성향 설정 요청 (원본과 동일)"""

    perspective: PerspectiveEnum


class UserRegistrationRequest(BaseModel):
    """새 사용자 등록 요청"""

    perspective: Optional[PerspectiveEnum] = Field(
        default=PerspectiveEnum.center, description="사용자의 정치성향"
    )
    previous_uid: Optional[str] = Field(
        default=None, description="마이그레이션할 이전 게스트 사용자 ID"
    )



class ProfileUploadUrlRequest(BaseModel):
    """프로필 이미지 업로드 URL 요청"""

    content_type: str = Field(
        ...,
        alias="contentType",
        description="이미지 MIME 타입 (image/jpeg, image/png, etc.)",
    )

    @field_validator("content_type")
    @classmethod
    def validate_content_type(cls, v: str) -> str:
        allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp"]
        if v not in allowed_types:
            raise ValueError(f"지원하지 않는 이미지 형식입니다. 허용: {', '.join(allowed_types)}")
        return v

    model_config = {"populate_by_name": True}


class ProfileCommitRequest(BaseModel):
    """프로필 이미지 업로드 완료 요청"""

    upload_key: str = Field(..., alias="uploadKey", description="업로드 키")

    model_config = {"populate_by_name": True}


class NotificationToggleRequest(BaseModel):
    """알림 설정 토글 요청"""

    enabled: bool = Field(..., description="알림 활성화 여부")

    model_config = {"populate_by_name": True}


class GlobalNotificationToggleRequest(BaseModel):
    """전역 알림 설정 토글 요청(부분 업데이트 허용)"""

    comment_like_enabled: Optional[bool] = Field(
        default=None, alias="commentLikeEnabled", description="댓글 좋아요 알림"
    )
    comment_reply_enabled: Optional[bool] = Field(
        default=None, alias="commentReplyEnabled", description="댓글 답글 알림"
    )
    major_comment_enabled: Optional[bool] = Field(
        default=None, alias="majorCommentEnabled", description="주요 댓글 알림"
    )
    issue_subscription_enabled: Optional[bool] = Field(
        default=None, alias="issueSubscriptionEnabled", description="이슈 구독 알림"
    )
    media_subscription_enabled: Optional[bool] = Field(
        default=None, alias="mediaSubscriptionEnabled", description="매체 구독 알림"
    )
    topic_subscription_enabled: Optional[bool] = Field(
        default=None, alias="topicSubscriptionEnabled", description="토픽 구독 알림"
    )

    model_config = {"populate_by_name": True}


class UserOnboardingRequest(BaseModel):
    """온보딩 시 초기 정치성향 점수 입력 요청"""

    perspective: PerspectiveEnum = Field(..., description="사용자의 정치성향")

    model_config = {"populate_by_name": True}

class UserEntitlementRequest(BaseModel):
    """사용자 권한 설정 요청"""

    entitlement: UserEntitlementEnum = Field(
        UserEntitlementEnum.free    )

    model_config = {"populate_by_name": True}