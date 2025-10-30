from enum import Enum


class CategoryEnum(str, Enum):
    """기사/이슈 카테고리"""

    politics = "politics"
    economy = "economy"
    society = "society"
    culture = "culture"
    international = "international"
    technology = "technology"


class PerspectiveEnum(str, Enum):
    """미디어 소스의 정치적 성향"""

    left = "left"
    center_left = "center_left"
    center = "center"
    center_right = "center_right"
    right = "right"


class EducationLevelEnum(str, Enum):
    """배경지식 난이도 레벨"""

    elementary = "elementary"  # 초등: 모든 것 (제한 없음)
    middle = "middle"  # 중등: difficulty >= 4
    high = "high"  # 고등: difficulty >= 7
