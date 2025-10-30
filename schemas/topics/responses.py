from typing import List, Optional

from pydantic import BaseModel, Field

from ..common.enums import CategoryEnum
from ..issues.responses import IssueListResponse
from .enums import TopicStatusEnum
from .models import RelatedTopicInfo
from uuid import uuid4

class TopicResponse(BaseModel):
    """토픽 응답 모델"""

    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    name: str = Field(..., min_length=1, max_length=50)
    category: CategoryEnum = Field(...)
    status: TopicStatusEnum = Field(default=TopicStatusEnum.ACTIVE, description="토픽 상태")
    score: float = Field(default=0.0, ge=0.0, description="토픽 점수")
    issues_count: Optional[int] = Field(None, alias="issuesCount", ge=0)
    is_subscribed: bool = Field(False, alias="isSubscribed")
    is_all_topic: Optional[bool] = Field(None, alias="isAllTopic", description="모든 카테고리 토픽 여부")

    model_config = {"populate_by_name": True}


class TopicListResponse(BaseModel):
    """토픽 목록 응답 모델"""

    topics: List[TopicResponse]
    has_more: bool = Field(..., alias="hasMore")
    last_topic_id: Optional[str] = Field(None, alias="lastTopicId")

    model_config = {"populate_by_name": True}


class TopicDetailResponse(TopicResponse):
    """토픽 상세 응답 모델"""

    issues: IssueListResponse
    related_topics: List[RelatedTopicInfo] = Field(..., alias="relatedTopics")


class TopicDetailListResponse(BaseModel):
    """토픽 상세 목록 응답 모델"""

    topics: List[TopicDetailResponse]
    has_more: bool = Field(..., alias="hasMore")
    last_topic_id: str = Field(..., alias="lastTopicId")

    model_config = {"populate_by_name": True}


class TopicsWithIssuesResponse(BaseModel):
    """토픽 목록과 이슈 목록을 포함하는 응답 모델"""

    topics: TopicListResponse = Field(..., description="토픽 목록")
    issues: IssueListResponse = Field(..., description="이슈 목록")

    model_config = {"populate_by_name": True}
