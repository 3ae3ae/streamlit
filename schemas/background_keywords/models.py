"""Background Keywords DB 모델"""

from datetime import datetime
from typing import Any, Dict, List
from pydantic import BaseModel, Field


class KeywordExtraction(BaseModel):
    """키워드 추출 결과 모델 (LLM 출력용)"""

    keyword: str = Field(..., description="추출된 키워드 텍스트")
    type: str = Field(..., description="키워드 타입 (PERSON, ORGANIZATION, LOCATION, TERM, EVENT)")
    difficulty: int = Field(..., ge=1, le=10, description="난이도 (1-10)")
    needs_explanation: bool = Field(..., alias="needsExplanation", description="배경지식 필요 여부")

    model_config = {"populate_by_name": True}


class KeywordExtractionList(BaseModel):
    """키워드 추출 결과 리스트 (LLM 출력용)"""

    extractions: List[KeywordExtraction] = Field(default_factory=list, description="추출된 키워드 리스트")


class KeywordDescription(BaseModel):
    """키워드 기본 설명 모델 (간결한 정의)"""

    description: str = Field(
        ...,
        description="키워드에 대한 간결한 설명 (100-150자, 학생 수준)"
    )


class ContextualSummary(BaseModel):
    """LLM이 생성하는 구조화된 배경지식 모델"""

    background_knowledge: str = Field(..., description="키워드에 대한 배경지식 설명")

class IssueReference(BaseModel):
    """키워드가 언급된 이슈 참조 (ID만 저장, 실제 데이터는 issues 컬렉션에서 조회)"""

    issue_id: str = Field(..., alias="issueId", description="이슈 ID")
    mentioned_at: datetime = Field(..., alias="mentionedAt", description="키워드 사용 시간")

    model_config = {"populate_by_name": True}


class ArticleMention(BaseModel):
    """키워드 관련 기사 정보"""

    article_id: str = Field(..., alias="articleId")
    title: str = Field(..., description="기사 제목")
    url: str = Field(..., description="기사 URL")
    published_at: datetime = Field(..., alias="publishedAt")

    model_config = {"populate_by_name": True}


class KeywordReference(BaseModel):
    """키워드 참조 정보 (lambda에서 사용)"""

    keyword_id: str = Field(..., alias="keywordId", description="backgroundKeywords 컬렉션의 ID")
    explanation: str = Field(default="", description="이슈별 맥락 배경지식 설명")
    difficulty: int = Field(..., description="키워드 난이도 (1-10)")
    span: Dict[str, Any] = Field(..., description="키워드 등장 위치 (field, start, end)")

    model_config = {"populate_by_name": True}
