"""Background Keywords Collection Models"""

from datetime import datetime
from typing import List
from uuid import uuid4

from pydantic import BaseModel, Field

from .models import IssueReference


class BackgroundKeyword(BaseModel):
    """
    배경지식 키워드 컬렉션 모델 (backgroundKeywords)

    전역적으로 관리되는 키워드 데이터베이스.
    여러 이슈에서 재사용 가능하며, 이슈 히스토리를 추적합니다.
    """

    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id", description="키워드 ID")
    keyword: str = Field(..., description="키워드 원문 (정규화됨)")
    type: str = Field(..., description="PERSON, ORGANIZATION, LOCATION, TERM, EVENT")
    difficulty: int = Field(..., ge=1, le=10, description="난이도 (1=쉬움, 10=어려움)")

    # 핵심 정보
    description: str = Field(..., description="키워드 기본 설명 (재사용 가능, Wikipedia/웹 검색)")

    # 이슈 히스토리 (이 키워드를 다룬 이슈들 - 이슈를 통해 관련 기사 추적 가능)
    issue_history: List[IssueReference] = Field(
        default_factory=list,
        alias="issueHistory",
        description="이 키워드가 등장한 이슈 목록 (최근 10개)",
    )

    # 메타데이터
    usage_count: int = Field(default=1, alias="usageCount", description="사용된 횟수")
    created_at: datetime = Field(default_factory=datetime.now, alias="createdAt", description="생성 시간")
    updated_at: datetime = Field(default_factory=datetime.now, alias="updatedAt", description="업데이트 시간")
    last_used_at: datetime = Field(default_factory=datetime.now, alias="lastUsedAt", description="마지막 사용 시간")

    # 정보 출처 (디버깅/개선용)
    source: str = Field(default="llm", description="db_cache|web_search|llm")

    model_config = {"populate_by_name": True}
