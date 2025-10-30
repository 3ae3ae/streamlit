from datetime import datetime
from uuid import uuid4
from typing import Optional

from pydantic import BaseModel, Field

from .enums import FeedbackTypeEnum, FeedbackStatusEnum


class Feedback(BaseModel):
    """사용자 피드백 모델"""

    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id", description="피드백 ID")
    user_id: str = Field(..., alias="userId", description="작성자 사용자 ID")
    inquiry_type: FeedbackTypeEnum = Field(..., alias="inquiryType", description="문의 유형")
    email: Optional[str] = Field(None, description="회신 이메일 (선택)")
    title: Optional[str] = Field(None, description="제목 (선택)")
    content: str = Field(..., description="내용")
    status: FeedbackStatusEnum = Field(default=FeedbackStatusEnum.PENDING, description="처리 상태")
    created_at: datetime = Field(default_factory=datetime.now, alias="createdAt", description="생성 시간")

    # User context (프론트 전송 값 저장용)
    user_email: Optional[str] = Field(None, alias="userEmail", description="사용자 이메일")
    is_anonymous: Optional[bool] = Field(None, alias="isAnonymous", description="익명 여부")
    auth_provider: Optional[str] = Field(None, alias="authProvider", description="인증 제공자")

    # App metadata
    app_version: Optional[str] = Field(None, alias="appVersion", description="앱 버전")
    build_number: Optional[str] = Field(None, alias="buildNumber", description="빌드 넘버")
    package_name: Optional[str] = Field(None, alias="packageName", description="패키지 네임")

    # Platform info
    platform: Optional[str] = Field(None, alias="platform", description="플랫폼")
    platform_version: Optional[str] = Field(None, alias="platformVersion", description="플랫폼 버전")
    is_android: Optional[bool] = Field(None, alias="isAndroid", description="안드로이드 여부")
    is_ios: Optional[bool] = Field(None, alias="isIOS", description="iOS 여부")

    model_config = {"populate_by_name": True}
