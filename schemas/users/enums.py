from enum import Enum


class UserEntitlementEnum(str, Enum):
    """사용자 유료 구독 등급"""

    free = "free"
    bronze = "bronze"
    silver = "silver"
    gold = "gold"
    platinum = "platinum"
