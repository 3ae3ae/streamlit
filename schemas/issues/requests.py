from pydantic import BaseModel, Field


class IssueEvaluationRequest(BaseModel):
    """이슈 정치성향 평가 요청"""

    perspective: str = Field(..., pattern="^(left|center|right)$")
