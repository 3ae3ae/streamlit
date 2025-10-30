from pydantic import BaseModel, Field

from uuid import uuid4
class RelatedTopicInfo(BaseModel):
    """관련 토픽 정보"""

    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    name: str
    is_subscribed: bool = Field(False, alias="isSubscribed")

    model_config = {"populate_by_name": True}
