from typing import Optional

from pydantic import BaseModel, Field


class QueryParams(BaseModel):
    """쿼리 파라미터 검증 모델"""

    limit: Optional[int] = Field(
        default=10, ge=1, le=50, description="한 번에 가져올 항목 수"
    )
    last_issue_id: Optional[str] = Field(
        None, alias="lastIssueId", description="마지막 이슈 ID (페이징용)"
    )

    model_config = {"populate_by_name": True}
