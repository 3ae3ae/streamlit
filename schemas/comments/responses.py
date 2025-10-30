from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from uuid import uuid4
from ..users.enums import UserEntitlementEnum

class CommentResponse(BaseModel):
    """메타 정보를 포함한 댓글 응답 모델 (불필요/중복 필드 제거)
    포함: id, content, createdAt, likeCount, isDeleted, source, nickname, imageUrl, isLiked, perspective
    제외: issueId, userId, parentCommentId
    """
    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id", description="댓글 ID")
    content: str = Field(..., description="댓글 내용")
    created_at: datetime = Field(..., alias="createdAt", description="생성 시간")
    like_count: int = Field(0, alias="likeCount", ge=0, description="좋아요 수")
    is_deleted: bool = Field(False, alias="isDeleted", description="삭제 여부")
    source: List[str] = Field(default_factory=list, description="댓글 출처 url")
    @field_validator("source", mode="before")
    def none_to_list(cls, v):
        return [] if v is None else v
    user_id: Optional[str] = Field(None, alias="userId", description="댓글 작성자 ID")
    nickname: Optional[str] = Field(None, description="댓글 작성자 닉네임")
    perspective: str = Field(..., pattern="^(left|center|right)$", description="댓글 성향")
    image_url: Optional[str] = Field(None, alias="imageUrl", description="댓글 작성자 프로필 이미지 URL")
    is_liked: bool = Field(False, alias="isLiked", description="현재 사용자의 좋아요 여부")
    is_reported: bool = Field(False, alias="isReported", description="현재 사용자가 신고한 댓글 여부")
    entitlement: Optional[UserEntitlementEnum] = Field(
        UserEntitlementEnum.free,
        description="댓글 작성자의 유료 구독 등급",
    )

    model_config = {"populate_by_name": True}


class CommentReply(CommentResponse):
    """답글 모델 (메타 포함)"""

    model_config = {"populate_by_name": True}


class CommentItem(CommentResponse):
    """최상위 댓글 모델 (답글 목록 포함)"""

    replies: List[CommentReply] = Field(default_factory=list, description="답글 목록")
    is_major: bool = Field(False, alias="isMajor", description="댓글 대표 여부")

    model_config = {"populate_by_name": True}


class CommentListResponse(BaseModel):
    """댓글 목록 응답"""

    perspective: str = Field(..., description="댓글창 (left|center|right)")
    comments_count: Optional[int] = Field(0, alias="commentsCount", description="댓글 수")
    comments: List[CommentItem] = Field(default_factory=list)
    has_more: bool = Field(False, alias="hasMore", description="다음 페이지 여부")
    last_comment_id: Optional[str] = Field(None, alias="lastCommentId", description="페이징용 마지막 댓글 ID")

    model_config = {"populate_by_name": True}


class MajorCommentItem(BaseModel):
    """메이저 댓글 응답 모델 (불필요/중복 제거)"""

    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id", description="댓글 ID")
    content: str = Field(..., description="댓글 내용")
    created_at: datetime = Field(..., alias="createdAt", description="생성 시간")
    is_deleted: bool = Field(False, alias="isDeleted", description="삭제 여부")
    source: List[str] = Field(default_factory=list, description="댓글 출처 url")
    perspective: str = Field(..., pattern="^(left|center|right)$", description="원래 댓글 성향")
    left_like_count: int = Field(0, alias="leftLikeCount", ge=0, description="좌성향 좋아요 수")
    center_like_count: int = Field(0, alias="centerLikeCount", ge=0, description="중도 좋아요 수")
    right_like_count: int = Field(0, alias="rightLikeCount", ge=0, description="우성향 좋아요 수")
    user_id: Optional[str] = Field(None, alias="userId", description="댓글 작성자 ID")
    nickname: Optional[str] = Field(None, description="댓글 작성자 닉네임")
    image_url: Optional[str] = Field(None, alias="imageUrl", description="댓글 작성자 프로필 이미지 URL")
    is_liked: bool = Field(False, alias="isLiked", description="현재 사용자의 좋아요 여부")
    replies: List["MajorCommentItem"] = Field(default_factory=list, description="답글 목록")
    entitlement: Optional[UserEntitlementEnum] = Field(
        UserEntitlementEnum.free,
        description="댓글 작성자의 유료 구독 등급",
    )

    model_config = {"populate_by_name": True}


class MajorCommentListResponse(BaseModel):
    """메이저 댓글 목록 응답"""

    comments: List[MajorCommentItem] = Field(default_factory=list)

    model_config = {"populate_by_name": True}
