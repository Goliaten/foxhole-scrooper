from dataclasses import dataclass, field
import math
from typing import List, Tuple
import cv2
import numpy as np


@dataclass
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
        # TODO allow scaling by resolution ratio
        pnt1 = np.array([self.c_x, self.c_y])
        if isinstance(inp, Bbox):
            pnt2 = np.array([inp.c_x, inp.c_y])
        elif isinstance(inp, (list, tuple)):
            pnt2 = np.array([inp[0], inp[1]])
        else:
            return float("inf")

        # print(f"{pnt1=}, {pnt2=}")
        return cv2.norm(
            pnt1,
            pnt2,
            cv2.NORM_L2,
        )

    def get_angle_from_centers(
        self,
        second_point: "Bbox" | Tuple[float, float],
        third_point: "Bbox" | Tuple[float, float],
    ) -> float:
        # TODO allow scaling by resolution ratio
        a = np.array([self.c_x, self.c_y])
        if isinstance(second_point, Bbox):
            b = np.array([second_point.c_x, second_point.c_y])
        elif isinstance(second_point, (list, tuple)):
            b = np.array([second_point[0], second_point[1]])

        if isinstance(third_point, Bbox):
            c = np.array([third_point.c_x, third_point.c_y])
        elif isinstance(third_point, (list, tuple)):
            c = np.array([third_point[0], third_point[1]])

        x = np.linalg.norm(a - b)
        y = np.linalg.norm(b - c)
        z = np.linalg.norm(a - c)
        angle = math.acos((x**2 + y**2 - z**2) / (2 * x * y))
        angle_360 = angle / (2 * math.pi) * 360
        angle_sign = angle_360 if a[0] > b[0] else -angle_360

        # print(f"{a=} {b=} {c=} {angle=} {angle_360=} {angle_sign=}")
        return angle_sign
