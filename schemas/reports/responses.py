from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, Field

from .enums import (
    ContentTypeEnum,
    ReportStatusEnum,
    CommentReportReasonEnum,
    IssueReportReasonEnum,
    UserReportReasonEnum,
)


class ReportItem(BaseModel):
    """신고 단일 항목 응답"""

    id: str = Field(..., alias="_id")
    content_id: str = Field(..., alias="contentId")
    content_type: ContentTypeEnum = Field(..., alias="contentType")
    reason: Union[
        IssueReportReasonEnum,
        UserReportReasonEnum,
        CommentReportReasonEnum,
    ]
    reporter_id: str = Field(..., alias="reporterId")
    reported_at: datetime = Field(..., alias="reportedAt")
    status: ReportStatusEnum
    admin_note: Optional[str] = Field(None, alias="adminNote")
    description: Optional[str] = None

    model_config = {"populate_by_name": True}


class ReportListResponse(BaseModel):
    """신고 목록 응답 (어드민용)"""

    reports: List[ReportItem]
    has_more: bool = Field(..., alias="hasMore")
    last_report_id: Optional[str] = Field(None, alias="lastReportId")

    model_config = {"populate_by_name": True}


