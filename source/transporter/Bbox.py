from dataclasses import dataclass, field
from typing import Tuple


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
