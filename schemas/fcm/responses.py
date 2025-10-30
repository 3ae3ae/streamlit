from typing import List, Optional

from pydantic import BaseModel, Field

from ..common.enums import CategoryEnum
from ..issues.models import ClusterMetadataAdmin, CoverageSpectrum, Tag
from ..media.responses import SourceInfoResponse
from ..articles.responses import ArticleListResponse
from uuid import uuid4

class FcmSendResponse(BaseModel):
    """FCM 전송 응답 모델(토픽/토큰 공용)"""

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

class FcmSubscribeResponse(BaseModel):
    """FCM 토픽 구독 응답 모델"""
    
    success: bool = Field(True, description="성공 여부")
    topic: str = Field(..., description="구독한 토픽 이름")
    success_count: int = Field(..., description="성공한 토큰 수")
    failure_count: int = Field(..., description="실패한 토큰 수")
    failed_tokens: Optional[List[dict]] = Field(None, description="실패한 토큰과 오류 목록")
    tokens_count: int = Field(..., description="구독 대상 토큰 총 수")
    
    model_config = {"populate_by_name": True}
    
class FcmUnsubscribeResponse(BaseModel):
    """FCM 토픽 구독 취소 응답 모델"""
    
    success: bool = Field(True, description="성공 여부")
    topic: str = Field(..., description="구독 취소한 토픽 이름")
    success_count: int = Field(..., description="성공한 토큰 수")
    failure_count: int = Field(..., description="실패한 토큰 수")
    failed_tokens: Optional[List[dict]] = Field(None, description="실패한 토큰과 오류 목록")
    tokens_count: int = Field(..., description="구독 취소 대상 토큰 총 수")
    
    model_config = {"populate_by_name": True}