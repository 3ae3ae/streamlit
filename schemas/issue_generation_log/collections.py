from pydantic import BaseModel, Field
from typing import Dict, Optional, List
from datetime import datetime


class EvidenceItem(BaseModel):
    """검증 근거 아이템"""
    article_index: int = Field(
        description="검증에 사용한 기사 인덱스",
        alias="articleIndex"
    )
    quote: str = Field(
        description="기사에서 직접 발췌한 근거 인용문"
    )
    article_url: Optional[str] = Field(
        default=None,
        description="근거 인용이 출처한 기사 URL",
        alias="articleUrl"
    )

    model_config = {
        "populate_by_name": True,
        "by_alias": True
    }


class PerspectiveValidation(BaseModel):
    """성향별 통합 검증 결과"""
    passed: Optional[bool] = Field(default=False, description="해당 성향의 전체 검증 통과 여부")
    # 인용 검증 결과
    citation_passed: Optional[bool] = Field(default=None, description="인용 검증 통과 여부", alias="citationPassed")
    citation_error: Optional[str] = Field(default=None, description="인용 검증 실패 사유", alias="citationError")
    citation_evidence: Optional[List[EvidenceItem]] = Field(default=None, description="인용 검증 근거", alias="citationEvidence")
    # 내용 검증 결과
    content_passed: Optional[bool] = Field(default=None, description="내용 검증 통과 여부", alias="contentPassed")
    content_error: Optional[str] = Field(default=None, description="내용 검증 실패 사유", alias="contentError")
    content_evidence: Optional[List[EvidenceItem]] = Field(default=None, description="내용 검증 근거", alias="contentEvidence")

    model_config = {
        "populate_by_name": True,
        "by_alias": True
    }


class ValidationResult(BaseModel):
    attempt: int = Field(default=0, description="시도 횟수 (0부터 시작)")
    changed_perspectives: List[str] = Field(default_factory=list, description="이번 시도에서 변경/재검증된 성향 목록", alias="changedPerspectives")
    perspectives: Dict[str, PerspectiveValidation] = Field(default_factory=dict)

    model_config = {
        "populate_by_name": True,
        "by_alias": True
    }

class RetryChanges(BaseModel):
    left_comparison: Optional[str] = Field(default=None, description="좌성향 비교 결과", alias="leftComparison")
    center_comparison: Optional[str] = Field(default=None, description="중도 비교 결과", alias="centerComparison")
    right_comparison: Optional[str] = Field(default=None, description="우성향 비교 결과", alias="rightComparison")
    validation_snapshot: Optional[ValidationResult] = Field(default=None, description="재시도 당시 검증 결과", alias="validationSnapshot")
    attempt_number: Optional[int] = Field(default=None, description="재시도 번호", alias="attemptNumber")

    model_config = {
        "populate_by_name": True,
        "by_alias": True  # 내부 모델도 카멜케이스로 직렬화
    }

class IssueGenerationLog(BaseModel):
    """이슈 생성 로그 - 재검토 변경사항에 검증 정보 포함"""
    issue_id: str = Field(description="이슈 ID", alias="issueId")
    retry_changes: Optional[List[RetryChanges]] = Field(default=None, description="재검토 변경사항(검증 정보 포함)", alias="retryChanges")
    initial_comparison: Optional[Dict[str, Optional[str]]] = Field(default=None, description="최초 전체 비교 결과 (값에 None 허용)", alias="initialComparison")
    final_comparison: Optional[Dict[str, Optional[str]]] = Field(default=None, description="최종 전체 비교 결과 (값에 None 허용)", alias="finalComparison")
    created_at: datetime = Field(default_factory=datetime.now, description="생성 시간", alias="createdAt")
    updated_at: datetime = Field(default_factory=datetime.now, description="수정 시간", alias="updatedAt")

    model_config = {
        "populate_by_name": True,
        "by_alias": True  # 내부 모델도 카멜케이스로 직렬화
    }