from pydantic import BaseModel, Field

from ..common.enums import CategoryEnum, PerspectiveEnum
from .models import Question, Option
from ..users.models import UserPoliticalScoreHistoryWithoutMetadata


class QuestionsGetResponse(BaseModel):
    questions: list[Question] = Field(default_factory=list)
    options: list[Option] = Field(default_factory=list)


class AnalyzeResponse(BaseModel):
    perspective: PerspectiveEnum = Field(..., description="분석된 전체 성향")
    summary: str = Field(..., description="요약 분석 멘트")
    dominant_category: CategoryEnum = Field(..., alias="dominantCategory", description="가장 두드러진 영역")
    scores: UserPoliticalScoreHistoryWithoutMetadata = Field(..., description="카테고리별 좌/중/우 점수")

    model_config = {"populate_by_name": True}

