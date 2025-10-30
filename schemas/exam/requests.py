from pydantic import BaseModel, Field


class AnswerItem(BaseModel):
    question_id: int = Field(..., alias="questionId", description="질문 ID")
    value: int = Field(..., ge=1, le=5, description="응답 값 (1~5)")

    model_config = {"populate_by_name": True}


class AnalyzeRequest(BaseModel):
    answers: list[AnswerItem] = Field(..., description="응답 항목 목록")

