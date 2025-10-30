"""
Issue Generation Log - Response Schemas
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from .collections import RetryChanges


class IssueGenerationLogAdminResponse(BaseModel):
    """관리자용 이슈 생성 로그 응답 모델"""
    issue_id: str = Field(alias="issueId")
    retry_changes: List[RetryChanges] = Field(default_factory=list, alias="retryChanges")
    count: int = Field(default=0, description="로그 항목 수", alias="count")
    created_at: Optional[datetime] = Field(default=None, alias="createdAt")
    updated_at: Optional[datetime] = Field(default=None, alias="updatedAt")

    model_config = {
        "populate_by_name": True,
        "by_alias": True 
    }


