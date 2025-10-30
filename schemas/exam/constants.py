from .models import Option

EXAM_OPTIONS: list[Option] = [
    Option(value=1, label="매우 반대"),
    Option(value=2, label="반대"),
    Option(value=3, label="보통"),
    Option(value=4, label="찬성"),
    Option(value=5, label="매우 찬성"),
]