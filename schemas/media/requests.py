from pydantic import BaseModel

from ..common.enums import PerspectiveEnum


class MediaPerspectiveEvaluationRequest(BaseModel):
    """매체 정치성향 평가 요청"""

    perspective: PerspectiveEnum


class SourcePerspectiveEvaluationRequest(BaseModel):
    """언론사 정치성향 평가 요청"""

    perspective: PerspectiveEnum
