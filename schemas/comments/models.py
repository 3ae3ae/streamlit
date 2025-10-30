from datetime import datetime

from pydantic import BaseModel, Field

from uuid import uuid4
class CommentBase(BaseModel):
    """댓글 모델"""

    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id", description="댓글 ID")
    user_id: str = Field(..., alias="userId", description="댓글 작성자 ID")
    content: str = Field(..., description="댓글 내용")
    created_at: datetime = Field(
        default_factory=datetime.now, alias="createdAt", description="생성 시간"
    )
    model_config = {"populate_by_name": True}
