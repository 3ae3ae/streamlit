from typing import Optional

from pydantic import BaseModel, Field

from .enums import FeedbackTypeEnum, FeedbackStatusEnum


class FeedbackCreateRequest(BaseModel):
    """피드백 생성 요청 바디"""

    inquiry_type: FeedbackTypeEnum = Field(..., alias="inquiryType", description="문의 유형")
    email: Optional[str] = Field(None, description="회신 이메일 (선택)")
    title: Optional[str] = Field(None, description="제목 (선택)")
    content: str = Field(..., description="내용")

    # User context
    user_email: Optional[str] = Field(
        None, alias="userEmail", description="사용자 이메일 (프론트 전송)"
    )
    is_anonymous: Optional[bool] = Field(
        None, alias="isAnonymous", description="익명 사용자 여부 (프론트 전송)"
    )
    auth_provider: Optional[str] = Field(
        None, alias="authProvider", description="인증 제공자 ID (프론트 전송)"
    )

    # App metadata
    app_version: Optional[str] = Field(
        None, alias="appVersion", description="앱 버전 (프론트 전송)"
    )
    build_number: Optional[str] = Field(
        None, alias="buildNumber", description="빌드 넘버 (프론트 전송)"
    )
    package_name: Optional[str] = Field(
        None, alias="packageName", description="패키지 네임 (프론트 전송)"
    )

    # Platform info
    platform: Optional[str] = Field(
        None, alias="platform", description="플랫폼(operatingSystem) (프론트 전송)"
    )
    platform_version: Optional[str] = Field(
        None, alias="platformVersion", description="플랫폼 버전 (프론트 전송)"
    )
    is_android: Optional[bool] = Field(
        None, alias="isAndroid", description="안드로이드 여부 (프론트 전송)"
    )
    is_ios: Optional[bool] = Field(
        None, alias="isIOS", description="iOS 여부 (프론트 전송)"
    )

    model_config = {"populate_by_name": True}


class FeedbackUpdateBody(BaseModel):
    """피드백 업데이트 바디 (어드민)"""

    status: Optional[FeedbackStatusEnum] = Field(None, description="처리 상태")

    model_config = {"populate_by_name": True}
