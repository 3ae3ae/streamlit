from enum import Enum


class FeedbackTypeEnum(str, Enum):
    """사용자 피드백 유형"""

    general = "general"  # 일반 문의
    feature = "feature"  # 기능 제안
    bug = "bug"  # 버그 신고
    content = "content"  # 콘텐츠 문의
    account = "account"  # 계정 관련
    other = "other"  # 기타


class FeedbackStatusEnum(str, Enum):
    """피드백 처리 상태"""

    PENDING = "pending"  # 처리 전
    IN_PROGRESS = "in_progress"  # 처리 중
    RESOLVED = "resolved"  # 처리 완료
