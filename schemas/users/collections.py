from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from ..common.enums import PerspectiveEnum
from .enums import UserEntitlementEnum
from .models import PoliticalPreferenceDetail

from uuid import uuid4
class User(BaseModel):
    """사용자 컬렉션 모델"""

    id: str = Field(default_factory=lambda: str(uuid4()), description="이메일 주소")
    nickname: Optional[str] = Field(
        "annonymous", description="사용자 닉네임", max_length=50, min_length=1
    )
    political_preference: Optional[PerspectiveEnum] = Field(
        PerspectiveEnum.center,
        alias="politicalPreference",
        description="사용자 정치성향",
    )
    entitlement: Optional[UserEntitlementEnum] = Field(
        UserEntitlementEnum.free,
        description="사용자 유료 구독 등급",
    )
    created_at: datetime = Field(default_factory=datetime.now, alias="createdAt", description="가입 시간")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt", description="수정 시간")
    accumulated_dasi_score: Optional[float] = Field(
        default=0.0,
        ge=0.0,
        alias="accumulatedDasiScore",
        description="누적 다시 스코어",
    )
    fcm_token: Optional[List[str]] = Field(None, alias="fcmToken", description="푸시 알림을 위한 FCM 토큰")
    profile_image_key: Optional[str] = Field(None, alias="profileImageKey", description="프로필 이미지 키")
    comment_like_notification_enabled: bool = Field(
        default=True,
        alias="commentLikeNotificationEnabled",
        description="댓글 좋아요 알림 설정 여부",
    )
    comment_reply_notification_enabled: bool = Field(
        default=True,
        alias="commentReplyNotificationEnabled",
        description="댓글 답글 알림 설정 여부",
    )
    major_comment_notification_enabled: bool = Field(
        default=True,
        alias="majorCommentNotificationEnabled",
        description="주요 댓글 알림 설정 여부",
    )
    media_subscription_notification_enabled: bool = Field(
        default=False,
        alias="mediaSubscriptionNotificationEnabled",
        description="매체 구독 알림 설정 여부",
    )
    topic_subscription_notification_enabled: bool = Field(
        default=True,
        alias="topicSubscriptionNotificationEnabled",
        description="토픽 구독 알림 설정 여부",
    )
    issue_subscription_notification_enabled: bool = Field(
        default=True,
        alias="issueSubscriptionNotificationEnabled",
        description="이슈 구독 알림 설정 여부",
    )

    model_config = {"populate_by_name": True}


class UserPoliticalPreferenceDetailHistory(BaseModel):
    """사용자 정치성향 기록 컬렉션 모델"""

    user_id: str = Field(..., alias="userId", description="사용자 이메일")
    recorded_at: datetime = Field(..., alias="recordedAt", description="기록된 시간")
    political_preference_detail: PoliticalPreferenceDetail = Field(
        ..., alias="politicalPreferenceDetail", description="정치성향"
    )

    model_config = {"populate_by_name": True}


class UserMediaSubscription(BaseModel):
    """사용자 매체 구독 컬렉션 모델"""

    user_id: str = Field(..., alias="userId", description="사용자 이메일")
    media_id: str = Field(..., alias="mediaId", description="매체 ID")
    subscribed_at: datetime = Field(default_factory=datetime.now, alias="subscribedAt", description="구독 시간")
    notification_enabled: bool = Field(default=False, alias="notificationEnabled", description="알림 설정 여부")

    model_config = {"populate_by_name": True}


class UserTopicSubscription(BaseModel):
    """사용자 토픽 구독 컬렉션 모델"""

    user_id: str = Field(..., alias="userId", description="사용자 이메일")
    topic_id: str = Field(..., alias="topicId", description="토픽 ID")
    subscribed_at: datetime = Field(default_factory=datetime.now, alias="subscribedAt", description="구독 시간")
    notification_enabled: bool = Field(True, alias="notificationEnabled", description="알림 설정 여부")

    model_config = {"populate_by_name": True}


class UserIssueSubscription(BaseModel):
    """사용자 이슈 구독 컬렉션 모델"""

    user_id: str = Field(..., alias="userId", description="사용자 이메일")
    issue_id: str = Field(..., alias="issueId", description="이슈 ID")
    subscribed_at: datetime = Field(default_factory=datetime.now, alias="subscribedAt", description="구독 시간")
    notification_enabled: bool = Field(True, alias="notificationEnabled", description="알림 설정 여부")

    model_config = {"populate_by_name": True}


class UserWatchHistory(BaseModel):
    """사용자 시청 기록 컬렉션 모델"""

    user_id: str = Field(..., alias="userId", description="사용자 아이디")
    issue_id: str = Field(..., alias="issueId", description="이슈 ID")
    watched_at: datetime = Field(default_factory=datetime.now, alias="watchedAt", description="시청 시간")

    model_config = {"populate_by_name": True}
