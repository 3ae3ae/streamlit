from enum import Enum


class SpectrumEnum(str, Enum):
    """질문에 대응되는 스펙트럼 (좌/중/우)

    exam.dart의 politicalSpectrum: 'left' | 'center' | 'right' 와 동일
    """

    left = "left"
    center = "center"
    right = "right"

