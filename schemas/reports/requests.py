from typing import Optional, Union
from pydantic import BaseModel, Field

from .enums import (
    ContentTypeEnum,
    CommentReportReasonEnum,
    ReportStatusEnum,
    IssueReportReasonEnum,
    UserReportReasonEnum,
)


class CreateReportRequest(BaseModel):
    """신고 생성 요청 바디"""

    content_id: str = Field(..., alias="contentId", description="신고 대상 콘텐츠 ID")
    content_type: ContentTypeEnum = Field(..., alias="contentType", description="콘텐츠 유형")
    reason: Union[
        IssueReportReasonEnum,
        UserReportReasonEnum,
        CommentReportReasonEnum,
    ] = Field(..., description="신고 사유")
    description: Optional[str] = Field(None, description="상세 설명 (선택)")

    model_config = {"populate_by_name": True}


class UpdateReportBody(BaseModel):
    """신고 업데이트 요청 바디"""

    status: Optional[ReportStatusEnum] = Field(None, description="신고 처리 상태")
    admin_note: Optional[str] = Field(None, description="관리자 메모")

    model_config = {"populate_by_name": True}


