from pydantic import BaseModel, Field
from typing import Optional

from ..common.enums import CategoryEnum
from .enums import SpectrumEnum


class Question(BaseModel):
    """정치 성향 테스트 질문 모델"""

    id: int = Field(..., description="질문 ID")
    text: str = Field(..., description="질문 내용")
    category: CategoryEnum = Field(..., description="질문 카테고리")
    spectrum: SpectrumEnum = Field(..., description="질문이 기여하는 스펙트럼(좌/중/우)")


class Option(BaseModel):
    """선택지(리커트 척도) 모델"""

    value: int = Field(..., ge=1, le=5, description="응답 값 (1~5)")
    label: str = Field(..., description="라벨")

