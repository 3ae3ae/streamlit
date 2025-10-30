from datetime import datetime

from pydantic import BaseModel, Field

from ..common.enums import CategoryEnum
from .enums import TopicStatusEnum
from uuid import uuid4

class Topic(BaseModel):
    """토픽 컬렉션 모델"""

    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id", description="토픽 ID")
    name: str = Field(..., min_length=1, max_length=50, description="토픽 이름")
    category: CategoryEnum = Field(..., description="토픽이 속한 카테고리")
    status: TopicStatusEnum = Field(default=TopicStatusEnum.ACTIVE, description="토픽 상태")
    score: float = Field(default=0.0, ge=0.0, description="토픽 점수")
    is_all_topic: bool = Field(False, alias="isAllTopic", description="모든 카테고리 토픽 여부")
    created_at: datetime = Field(..., alias="createdAt", description="생성 시간")
    updated_at: datetime = Field(..., alias="updatedAt", description="수정 시간")

    model_config = {"populate_by_name": True}


class TopicIssue(BaseModel):
    """토픽-이슈 관계 컬렉션 모델 (다대다 관계)"""

    topic_id: str = Field(..., alias="topicId", description="토픽 ID")
    issue_id: str = Field(..., alias="issueId", description="이슈 ID")
    connection_score: float = Field(
        default=0.0, ge=0.0, alias="connectionScore", description="연결 점수"
    )
    created_at: datetime = Field(default_factory=datetime.now, alias="createdAt", description="관계 생성 시간")
    issue_created_at: datetime = Field(
        default_factory=datetime.now,
        alias="issueCreatedAt",
        description="이슈 생성 시간",
    )

    model_config = {"populate_by_name": True}
