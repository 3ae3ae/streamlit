from enum import Enum


class ArticleStatusEnum(str, Enum):
    """기사 처리 상태"""

    PENDING = "pending"  # 처리 대기 중
    PREPROCESSED = "preprocessed"  # 전처리 완료
    EMBEDDED = "embedded"  # 임베딩 완료
