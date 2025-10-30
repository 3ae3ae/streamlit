from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from ..common.enums import CategoryEnum


class PoliticalScore(BaseModel):
    """정치성향 점수 모델"""

    left: float = Field(50.0, description="좌성향 점수")
    center: float = Field(50.0, description="중도 점수")
    right: float = Field(50.0, description="우성향 점수")

    model_config = {"populate_by_name": True}


class PoliticalScoreIncrement(BaseModel):
    """정치성향 점수 증가 모델"""

    category: CategoryEnum = Field(
        ...,
        description="정치성향 카테고리 (politics, economy, society, culture, technology, international)",
    )
    left: float = Field(0.0, description="좌성향 점수 증가")
    center: float = Field(0.0, description="중도 점수 증가")
    right: float = Field(0.0, description="우성향 점수 증가")

    model_config = {"populate_by_name": True}


class PoliticalScoreIncrementList(BaseModel):
    increments: List[PoliticalScoreIncrement] = Field(
        default_factory=list, description="정치성향 점수 증가 목록"
    )


class UserPoliticalScoreHistoryWithoutMetadata(BaseModel):
    politics: PoliticalScore = Field(default_factory=PoliticalScore, description="정치 분야 성향 점수")
    economy: PoliticalScore = Field(default_factory=PoliticalScore, description="경제 분야 성향 점수")
    society: PoliticalScore = Field(default_factory=PoliticalScore, description="사회 분야 성향 점수")
    culture: PoliticalScore = Field(default_factory=PoliticalScore, description="생활/문화 분야 성향 점수")
    technology: PoliticalScore = Field(default_factory=PoliticalScore, description="IT/과학 분야 성향 점수")
    international: PoliticalScore = Field(
        default_factory=PoliticalScore, description="세계 분야 성향 점수"
    )

    model_config = {"populate_by_name": True}


class Period(BaseModel):
    year: Optional[int] = Field(default_factory=datetime.now().year, description="연도")
    month: Optional[int] = Field(None, description="월")
    week: Optional[int] = Field(None, ge=1, le=5, description="주차 (1~5)")
    weekday: Optional[int] = Field(None, ge=0, le=6, description="요일 (0~6, 0=일요일, 6=토요일)")
    day: Optional[int] = Field(None, ge=1, le=31, description="일 (1~31)")

class UserPoliticalScoreHistory(UserPoliticalScoreHistoryWithoutMetadata):
    """전체 정치성향 점수 모델"""

    created_at: datetime = Field(
        default_factory=datetime.now, alias="createdAt", description="생성 시간"
    )
    user_id: str = Field(..., alias="userId", description="사용자 이메일")

    model_config = {"populate_by_name": True}

class PoliticalPreferenceDetail(BaseModel):
    """카테고리별 상세 정치성향 점수"""

    politics: List[int] = Field(
        ...,
        min_length=3,
        max_length=3,
        description="정치 분야 성향 점수 [좌성향, 중도, 우성향]",
    )
    economy: List[int] = Field(
        ...,
        min_length=3,
        max_length=3,
        description="경제 분야 성향 점수 [좌성향, 중도, 우성향]",
    )
    society: List[int] = Field(
        ...,
        min_length=3,
        max_length=3,
        description="사회 분야 성향 점수 [좌성향, 중도, 우성향]",
    )
    culture: List[int] = Field(
        ...,
        min_length=3,
        max_length=3,
        description="생활/문화 분야 성향 점수 [좌성향, 중도, 우성향]",
    )
    technology: List[int] = Field(
        ...,
        min_length=3,
        max_length=3,
        description="IT/과학 분야 성향 점수 [좌성향, 중도, 우성향]",
    )
    international: List[int] = Field(
        ...,
        min_length=3,
        max_length=3,
        description="세계 분야 성향 점수 [좌성향, 중도, 우성향]",
    )
