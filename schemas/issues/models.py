from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, Field


class CoverageSpectrum(BaseModel):
    """정치적 스펙트럼 분포"""

    left: int = Field(default=0, ge=0, description="좌성향(left, center_left) 기사 개수")
    center_left: int = Field(default=0, ge=0, description="중도 좌성향 기사 개수")
    center: int = Field(default=0, ge=0, description="중도 성향 기사 개수")
    center_right: int = Field(default=0, ge=0, description="중도 우성향 기사 개수")
    right: int = Field(default=0, ge=0, description="우성향(center_right, right) 기사 개수")
    total: int = Field(default=0, ge=0, description="전체 기사 개수")


class Tag(BaseModel):
    """이슈 태그 모델"""

    name: str = Field(..., description="태그 이름")
    color: str = Field("000000", description="태그 색상")


class ClusterMetadata(BaseModel):
    """이슈 클러스터링 메타데이터"""

    centroid: Optional[List[float]] = Field(None, description="이슈 임베딩 벡터 (클러스터링용)")
    is_newly_created: Optional[bool] = Field(None, alias="isNewlyCreated", description="새로 생성된 이슈 여부")
    has_new_articles: Optional[bool] = Field(None, alias="hasNewArticles", description="새로운 기사가 있는지 여부")
    modularity_gain: Optional[float] = Field(
        None, alias="modularityGain", description="클러스터링 모듈성 증가량 (0~1)"
    )
    max_similarity: Optional[float] = Field(
        None,
        alias="maxSimilarity",
        description="가장 유사한 기존 이슈와의 유사도 (0~1)",
    )

    model_config = {"populate_by_name": True}


class ClusterMetadataAdmin(BaseModel):
    """관리자용 이슈 클러스터링 메타데이터 (centroid 제외)"""

    is_newly_created: Optional[bool] = Field(
        None, alias="isNewlyCreated", description="새로 생성된 이슈 여부"
    )
    has_new_articles: Optional[bool] = Field(
        None, alias="hasNewArticles", description="새로운 기사가 있는지 여부"
    )
    modularity_gain: Optional[float] = Field(
        None, alias="modularityGain", description="클러스터링 모듈성 증가량 (0~1)"
    )
    max_similarity: Optional[float] = Field(
        None,
        alias="maxSimilarity",
        description="가장 유사한 기존 이슈와의 유사도 (0~1)",
    )

    model_config = {"populate_by_name": True}


class IssueImageItem(BaseModel):
    """
    이슈 대표/후보 이미지 항목 모델

    - 기사 원문 URL과 이미지 URL, 출처/발행 정보를 포함합니다.
    """

    source_url: str = Field(..., alias="sourceUrl", description="기사 원문 URL")
    image_url: str = Field(..., alias="imageUrl", description="기사 대표 이미지 URL")
    source_id: str = Field(..., alias="sourceId", description="언론사 소스 ID")
    source_name: Optional[str] = Field(None, alias="sourceName", description="언론사 이름")
    published_at: Optional[datetime] = Field(
        None, alias="publishedAt", description="기사 발행 시각"
    )

    model_config = {"populate_by_name": True}


class ImagesByPerspective(BaseModel):
    """
    성향별 이미지 후보 목록

    - 좌/중도/우 성향 그룹별 최대 N개 이미지 후보를 저장합니다.
    """

    left: List[IssueImageItem] = Field(default_factory=list, description="좌 성향 후보")
    center: List[IssueImageItem] = Field(default_factory=list, description="중도 성향 후보")
    right: List[IssueImageItem] = Field(default_factory=list, description="우 성향 후보")

    model_config = {"populate_by_name": True}


class KeywordRef(BaseModel):
    """특정 필드 내에서의 키워드 참조 정보"""

    keyword_id: str = Field(..., alias="keywordId", description="backgroundKeywords 컬렉션의 ID")
    explanation: str = Field(default="", description="이 이슈에 대한 배경지식 설명 (GPT 생성, 이슈별로 다름)")
    difficulty: int = Field(default=0, description="키워드 난이도 (1-10, 기존 데이터는 0)")
    start: int = Field(..., description="시작 인덱스 (inclusive)")
    end: int = Field(..., description="종료 인덱스 (exclusive)")

    model_config = {"populate_by_name": True}


class BackgroundKeywordRefs(BaseModel):
    """필드별로 그룹화된 배경지식 키워드 참조"""

    summary: List[KeywordRef] = Field(default_factory=list, description="요약에 등장하는 키워드들")
    left_comparison: List[KeywordRef] = Field(
        default_factory=list, alias="leftComparison", description="좌측 비교 텍스트의 키워드들"
    )
    center_comparison: List[KeywordRef] = Field(
        default_factory=list, alias="centerComparison", description="중도 비교 텍스트의 키워드들"
    )
    right_comparison: List[KeywordRef] = Field(
        default_factory=list, alias="rightComparison", description="우측 비교 텍스트의 키워드들"
    )

    model_config = {"populate_by_name": True}
