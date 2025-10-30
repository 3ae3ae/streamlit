from datetime import datetime
from typing import Union

from pydantic import BaseModel, Field
from typing import Optional
from ..reports.enums import (
    CommentReportReasonEnum,
    IssueReportReasonEnum,
    UserReportReasonEnum,
    ReportStatusEnum
)
from uuid import uuid4


class ReportedContents(BaseModel):
    """신고된 콘텐츠 모델"""

    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id", description="신고 ID")
    content_id: str = Field(
        ...,
        alias="contentId",
        description="신고된 콘텐츠 ID (ObjectId일 경우 str로 변환)",
    )
    content_type: str = Field(..., alias="contentType", description="콘텐츠 유형")
    reason: Union[
        IssueReportReasonEnum,
        UserReportReasonEnum,
        CommentReportReasonEnum,
    ] = Field(..., description="신고 사유")
    reporter_id: str = Field(..., alias="reporterId", description="신고자 ID")
    reported_at: datetime = Field(
        default_factory=datetime.now, alias="reportedAt", description="신고 시간"
    )
    status: ReportStatusEnum = Field(
        default=ReportStatusEnum.PENDING,
        description="신고 상태",
    )
    admin_note: Optional[str] = Field(
        None, alias="adminNote", description="관리자 메모"
    )

    model_config = {"populate_by_name": True}


class ArticleIssueLog(BaseModel):
    """기사-이슈 연결 로그"""

    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    article_id: str = Field(..., alias="articleId")
    issue_id: str = Field(..., alias="issueId")
    action: str = Field(...)  # "connect" or "disconnect"
    user_id: str = Field(..., alias="userId")
    timestamp: datetime = Field(default_factory=datetime.now)

    model_config = {"populate_by_name": True}
