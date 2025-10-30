from enum import Enum
from typing import Optional

class ReportStatusEnum(str, Enum):
    PENDING = "pending"  # 처리 대기 중
    DISMISSED = "dismissed"  # 기각됨
    ACTIONED = "actioned"  # 조치됨 (예: 콘텐츠 삭제)


class CommonReportReasonEnum(str, Enum):
    FALSE_INFORMATION = "허위 정보"
    SPAM_ADVERTISEMENT = "스팸/광고성 콘텐츠"
    SEXUAL_CONTENT = "선정적/음란물"
    VIOLENCE_HATE = "폭력적/혐오적 표현"
    DISCRIMINATION = "차별/혐오 발언"
    PERSONAL_INFORMATION = "개인정보 노출"
    COPYRIGHT_INFRINGEMENT = "저작권 침해"
    DEFAMATION = "명예훼손/비방"
    ILLEGAL_ACTIVITY = "불법 행위 조장"
    OTHER = "기타 부적절한 내용"


class NewsReportReasonEnum(str, Enum):
    MISLEADING_TITLE = "낚시성 제목"
    DISTORTION = "악의적 왜곡/오보"
    MANIPULATED_IMAGE = "조작/합성 이미지"
    PORTRAIT_RIGHTS = "초상권 침해"
