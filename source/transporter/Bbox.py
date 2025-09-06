from dataclasses import dataclass, field
from typing import List, Tuple
import cv2
import numpy as np


@dataclass(frozen=True)
class Bbox:
    x: float
    y: float
    w: float
    h: float
    c_x: float = field(init=False)
    c_y: float = field(init=False)
    is_relative: bool = field(default=False)

    def __post_init__(self):
        self.c_x = self.x + self.w / 2
        self.c_y = self.y + self.h / 2

    def to_relative(self, dimensions: Tuple[int, int]) -> "Bbox":
        return Bbox(
            self.x / dimensions[0],
            self.y / dimensions[1],
            self.w / dimensions[0],
            self.h / dimensions[1],
            is_relative=True,
        )

    def to_absolute(self, dimensions: Tuple[int, int]) -> "Bbox":
        return Bbox(
            int(self.x * dimensions[0]),
            int(self.y * dimensions[1]),
            int(self.w * dimensions[0]),
            int(self.h * dimensions[1]),
        )

    def to_list(self) -> List[float]:
        return [self.x, self.y, self.w, self.h]

    def get_distance_from_centers(self, inp: "Bbox" | Tuple[float, float]) -> float:
        if isinstance(inp, Bbox):
            return cv2.norm(
                np.array([self.c_x, self.c_y]),
                np.array([inp.c_x, inp.c_y]),
                cv2.NORM_L2,
            )
        elif isinstance(inp, (list, tuple)):
            return cv2.norm(
                np.array([self.c_x, self.c_y]),
                np.array([inp[0], inp[1]]),
                cv2.NORM_L2,
            )
        else:
            return float("inf")
