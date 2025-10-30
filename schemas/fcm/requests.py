from typing import List, Optional

from pydantic import BaseModel, Field



class FCMRegisterRequest(BaseModel):
    token: str = Field(..., description="디바이스 FCM 토큰")

class FcmSendRequest(BaseModel):
    """FCM 전송 요청 모델"""

    title: str = Field(description="알림 제목")
    body: str = Field(description="알림 본문")
    type: Optional[str] = Field("Send", description="알림 타입")
    image: Optional[str] = Field(None, description="알림 이미지 URL")
    data: Optional[dict[str, str]] = Field(None, description="데이터 페이로드(문자열 키/값)")
    topic: Optional[str] = Field(None, description="전송할 토픽 이름(없으면 기본 allUserTopic)")
    tokens: Optional[List[str]] = Field(None, description="전송 대상 디바이스 토큰 목록")

    model_config = {"populate_by_name": True}
    
class FcmSubscribeRequest(BaseModel):
    """FCM 토픽 구독 요청 모델"""
    
    topic: str = Field(..., description="구독할 토픽 이름")
    type: Optional[str] = Field("Subscribe", description="요청 타입")
    tokens: List[str] = Field(..., description="구독할 디바이스 토큰 목록")
    
    model_config = {"populate_by_name": True}
    
class FcmUnsubscribeRequest(BaseModel):
    """FCM 토픽 구독 취소 요청 모델"""
    
    topic: str = Field(..., description="구독 취소할 토픽 이름")
    type: Optional[str] = Field("Unsubscribe", description="요청 타입")
    tokens: List[str] = Field(..., description="구독 취소할 디바이스 토큰 목록")
    
    model_config = {"populate_by_name": True}