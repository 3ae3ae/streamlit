from enum import Enum


class TopicStatusEnum(str, Enum):
    """토픽 상태"""

    ACTIVE = "active"  # 현재 활발한 토픽 (상위 랭킹 내)
    PERSISTENT = "persistent"  # 영구 보존 토픽
    DORMANT = "dormant"  # 휴면 토픽 (순위 밖이지만 최근 활동)
    INACTIVE = "inactive"  # 비활성 토픽
