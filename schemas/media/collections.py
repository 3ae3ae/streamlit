from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from ..common.enums import PerspectiveEnum
from .models import CategoryInfo
from uuid import uuid4

class MediaSource(BaseModel):
    """미디어 소스 컬렉션 모델"""

    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id", description="미디어 소스 ID")
    name: str = Field(..., description="미디어 소스 이름")
    perspective: PerspectiveEnum = Field(..., description="정치적 성향")
    description: Optional[str] = Field(None, description="미디어 소스 설명")
    website_url: Optional[str] = Field(None, alias="websiteUrl", description="웹사이트 URL")
    founded_year: Optional[int] = Field(None, alias="foundedYear", description="설립 연도")
    ownership_info: Optional[str] = Field(None, alias="ownershipInfo", description="소유권 정보")
    created_at: datetime = Field(default_factory=datetime.now, alias="createdAt", description="등록 시간")
    category_list: Optional[List[CategoryInfo]] = Field(
        default_factory=list, alias="category_list", description="카테고리 목록"
    )
    ai_evaluated_perspective: Optional[PerspectiveEnum] = Field(
        None, alias="aiEvaluatedPerspective", description="AI가 평가한 성향"
    )
    expert_evaluated_perspective: Optional[PerspectiveEnum] = Field(
        None, alias="expertEvaluatedPerspective", description="전문가가 평가한 성향"
    )
    logo_url: str = Field(..., alias="logoUrl", description="로고 URL")

    model_config = {"populate_by_name": True}


class UserMediaEvaluation(BaseModel):
    """사용자 매체 평가 컬렉션 모델"""

    user_id: str = Field(..., alias="userId", description="사용자 이메일")
    media_id: str = Field(..., alias="mediaId", description="매체 ID")
    perspective: PerspectiveEnum = Field(..., description="평가한 성향")
    evaluated_at: datetime = Field(default_factory=datetime.now, alias="evaluatedAt", description="평가 시간")

    model_config = {"populate_by_name": True}


class UserSourceEvaluation(BaseModel):
    """사용자 언론사 평가 컬렉션 모델"""

    user_id: str = Field(..., alias="userId", description="사용자 ID")
    source_id: str = Field(..., alias="sourceId", description="언론사 ID")
    perspective: PerspectiveEnum = Field(..., description="평가한 성향")
    evaluated_at: datetime = Field(default_factory=datetime.now, alias="evaluatedAt", description="평가 시간")

    model_config = {"populate_by_name": True}
