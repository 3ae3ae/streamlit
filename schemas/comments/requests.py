from typing import Optional, List, Literal

from pydantic import BaseModel, Field


class CommentCreateRequest(BaseModel):
    """댓글 생성 요청"""

    content: str = Field(..., description="댓글 내용", max_length=500)
    parent_comment_id: Optional[str] = Field(
        None, alias="parentCommentId", description="부모 댓글 ID (답글 작성 시)"
    )
    source: List[str] = Field(default_factory=list, description="댓글 출처 URL")

    model_config = {"populate_by_name": True}


class MajorCommentRecalculateRequest(BaseModel):
    """대표 의견 재계산 Lambda 이벤트 페이로드"""

    type: Literal["RecalculateMajorComments"] = Field(
        "RecalculateMajorComments", description="이벤트 타입"
    )
    issue_id: str = Field(..., alias="issueId", description="대상 이슈 ID")

    model_config = {"populate_by_name": True}


class MajorCommentPromoteRequest(BaseModel):
    """대표 의견 승격 Lambda 이벤트 페이로드"""

    type: Literal["PromoteMajorComment"] = Field(
        "PromoteMajorComment", description="이벤트 타입"
    )
    comment_id: str = Field(..., alias="commentId", description="대상 댓글 ID")
    skip_recalc: bool = Field(False, alias="skipRecalc", description="재계산 생략 여부")

    model_config = {"populate_by_name": True}
