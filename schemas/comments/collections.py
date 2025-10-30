from typing import Optional, List

from pydantic import Field

from .models import CommentBase
from .enums import CommentStatusEnum


class IssueComments(CommentBase):
    """이슈 댓글 모델"""

    issue_id: str = Field(..., alias="issueId", description="이슈 ID")
    parent_comment_id: Optional[str] = Field(
        None, alias="parentCommentId", description="부모 댓글 ID (답글인 경우)"
    )
    perspective: str = Field(..., pattern="^(left|center|right)$", description="사용자 성향")
    is_deleted: bool = Field(False, alias="isDeleted", description="삭제 여부")
    status: CommentStatusEnum = Field(
        default=CommentStatusEnum.NORMAL,
        description="댓글 상태 (normal | major | ai_verified | major_blocked)",
    )
    # 메이저 댓글의 성향별 버킷 카운트 (메이저가 아닌 경우 0)
    left_like_count: int = Field(0, alias="leftLikeCount", ge=0, description="좌성향 좋아요 수")
    center_like_count: int = Field(
        0, alias="centerLikeCount", ge=0, description="중도 좋아요 수"
    )
    right_like_count: int = Field(
        0, alias="rightLikeCount", ge=0, description="우성향 좋아요 수"
    )
    source: List[str] = Field(default_factory=list, description="댓글 출처 url")
    is_verified: Optional[bool] = Field(
        False, alias="isVerified", description="AI 검증 여부 (검증 전: null, 검증 완료: true/false)"
    )
    highscore: Optional[int] = Field(
        0, ge=0, description="좋아요 최고기록")
    was_major: Optional[bool] = Field(
        False, alias="wasMajor", description="과거 메이저 댓글 여부"
    )

    model_config = {"populate_by_name": True}
