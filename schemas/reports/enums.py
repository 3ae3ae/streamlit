from enum import Enum

class ReportStatusEnum(str, Enum):
    PENDING = "pending"  # 처리 대기 중
    DISMISSED = "dismissed"  # 기각됨
    ACTIONED = "actioned"  # 조치됨 (예: 콘텐츠 삭제)
class ContentTypeEnum(str, Enum):
    """콘텐츠 유형 Enum"""
    COMMENT = "comment"
    ISSUE = "issue"
    USER = "user"

class CommentReportReasonEnum(str, Enum):
    ABUSIVE_LANGUAGE = "욕설/비속어"
    FLOODING = "도배성 댓글"
    HARASSMENT = "특정 이용자 괴롭힘"
    FALSE_SOURCE = "잘못된 출처"
    SPAM_ADVERTISEMENT = "스팸/광고성 콘텐츠"
    SEXUAL_CONTENT = "선정적/음란물"
    VIOLENCE_HATE = "폭력적/혐오적 표현"
    DISCRIMINATION = "차별/혐오 발언"
    PERSONAL_INFORMATION = "개인정보 노출"
    DEFAMATION = "명예훼손/비방"
    OTHER = "기타 부적절한 내용"

class UserReportReasonEnum(str, Enum):
    IMPERSONATION = "사칭/허위 신원"
    SPAM_ADVERTISEMENT = "스팸/광고"
    SEXUAL_CONTENT = "선정적/음란물"
    VIOLENCE_HATE = "폭력적/혐오적 표현"
    HARASSMENT = "괴롭힘/스토킹"
    PERSONAL_INFORMATION = "개인정보 노출"
    DEFAMATION = "명예훼손/비방"
    ILLEGAL_ACTIVITY = "불법 행위 조장"
    OTHER = "기타 부적절한 행동"

class IssueReportReasonEnum(str, Enum):
    MISLEADING_TITLE = "낚시성 제목"
    DISTORTION = "왜곡/오보"
    FALSE_INFORMATION = "허위 정보"
    SPAM_ADVERTISEMENT = "스팸/광고성 콘텐츠"
    SEXUAL_CONTENT = "선정적/음란물"
    VIOLENCE_HATE = "폭력적 표현"
    DISCRIMINATION = "차별/혐오 발언"
    DEFAMATION = "명예훼손/비방"
    ILLEGAL_ACTIVITY = "불법 행위 조장"
    INCORRECT_IMAGE = "내용과 맞지 않는 이미지"
    PORTRAIT_RIGHTS = "초상권 침해"
    OTHER = "기타 부적절한 내용"
