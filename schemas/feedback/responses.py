from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from .enums import FeedbackTypeEnum, FeedbackStatusEnum


class FeedbackItem(BaseModel):
    """피드백 단일 항목 응답"""

    id: str = Field(..., alias="_id")
    user_id: str = Field(..., alias="userId")
    inquiry_type: FeedbackTypeEnum = Field(..., alias="inquiryType")
    email: Optional[str] = None
    title: Optional[str] = None
    content: str
    status: FeedbackStatusEnum
    created_at: datetime = Field(..., alias="createdAt")
    nickname: Optional[str] = Field(None, description="작성자 닉네임 (어드민 목록용)")

    # User/App/Platform metadata (확장 정보)
    user_email: Optional[str] = Field(None, alias="userEmail")
    is_anonymous: Optional[bool] = Field(None, alias="isAnonymous")
    auth_provider: Optional[str] = Field(None, alias="authProvider")

    app_version: Optional[str] = Field(None, alias="appVersion")
    build_number: Optional[str] = Field(None, alias="buildNumber")
    package_name: Optional[str] = Field(None, alias="packageName")

    platform: Optional[str] = Field(None, alias="platform")
    platform_version: Optional[str] = Field(None, alias="platformVersion")
    is_android: Optional[bool] = Field(None, alias="isAndroid")
    is_ios: Optional[bool] = Field(None, alias="isIOS")

    model_config = {"populate_by_name": True}


class FeedbackListResponse(BaseModel):
    """피드백 목록 응답 (어드민용)"""

    feedbacks: List[FeedbackItem]
    has_more: bool = Field(..., alias="hasMore")
    last_feedback_id: Optional[str] = Field(None, alias="lastFeedbackId")

    model_config = {"populate_by_name": True}
