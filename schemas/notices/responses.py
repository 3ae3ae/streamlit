from typing import List, Optional

from pydantic import BaseModel, Field
from datetime import datetime
from uuid import uuid4
class NoticeResponse(BaseModel):
    """공지사항 응답 모델"""

    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    title: str = Field(..., description="공지사항 제목")
    content: Optional[str] = Field(None, description="공지사항 내용 (isImage가 True면 선택사항)")
    url: str = Field(..., description="공지사항 URL")
    is_image: bool = Field(..., alias="isImage", description="이미지 여부")
    is_important: bool = Field(..., alias="isImportant", description="중요 공지 여부")
    is_active: bool = Field(..., alias="isActive", description="활성화 여부")
    created_at: datetime = Field(..., alias="createdAt", description="생성 시간")
    updated_at: Optional[datetime] = Field(
        None, alias="updatedAt", description="수정 시간"
    )

    model_config = {"populate_by_name": True}
    
class NoticeListResponse(BaseModel):
    """공지사항 목록 응답 모델"""

    notices: List["NoticeWithoutContentResponse"] = Field(
        default_factory=list, description="공지사항 목록"
    )
    has_more: bool = Field(..., alias="hasMore", description="추가 공지사항 여부")
    last_notice_id: Optional[str] = Field(
        None, alias="lastNoticeId", description="마지막 공지사항 ID"
    )

    model_config = {"populate_by_name": True}
    
class NoticeWithoutContentResponse(BaseModel):
    """공지사항 응답 모델 (내용 제외)"""

    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    title: str = Field(..., description="공지사항 제목")
    url: str = Field(..., description="공지사항 URL")
    is_image: bool = Field(..., alias="isImage", description="이미지 여부")
    is_important: bool = Field(..., alias="isImportant", description="중요 공지 여부")
    is_active: bool = Field(..., alias="isActive", description="활성화 여부")
    created_at: datetime = Field(..., alias="createdAt", description="생성 시간")
    updated_at: Optional[datetime] = Field(
        None, alias="updatedAt", description="수정 시간"
    )

    model_config = {"populate_by_name": True}


class ActiveNoticesResponse(BaseModel):
    """활성화된 공지사항 목록 응답 모델"""

    notice_list: List[NoticeResponse] = Field(
        default_factory=list, alias="noticeList", description="활성화된 공지사항 목록"
    )

    model_config = {"populate_by_name": True}