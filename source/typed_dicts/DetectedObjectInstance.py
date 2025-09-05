from typing import Tuple, TypedDict


class DetectedObjectInstance(TypedDict):
    box: Tuple[int, int, int, int]
