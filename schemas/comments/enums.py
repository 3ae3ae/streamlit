from enum import Enum


class CommentStatusEnum(str, Enum):
    """댓글 상태 Enum
    - normal: 일반 상태
    - major: 대표의견 선정됨
    - major_forced: 관리자에 의해 강제 대표의견(순위와 무관하게 유지)
    - ai_verified: AI 검증 완료 상태
    - major_blocked: 대표의견으로 승격 불가(차단)
    """

    NORMAL = "normal"
    MAJOR = "major"
    MAJOR_FORCED = "major_forced"
    AI_VERIFIED = "ai_verified"
    MAJOR_BLOCKED = "major_blocked"


