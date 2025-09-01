from abc import ABC, abstractmethod

import toml
from source.modules.BaseModule import BaseModule
import config as cfg


class BaseMovementController(ABC, BaseModule):
    def __init__(self):
        super().__init__()
        with open(cfg.LOCATIONS_PATH, "r") as file:
            self.locations = toml.load(file)

    @abstractmethod
    def walk_up(self, period: float) -> None: ...

    @abstractmethod
    def walk_right(self, period: float) -> None: ...

    @abstractmethod
    def walk_left(self, period: float) -> None: ...

    @abstractmethod
    def walk_down(self, period: float) -> None: ...

    @abstractmethod
    def rotate_right(self, period: float) -> None: ...

    @abstractmethod
    def rotate_left(self, period: float) -> None: ...

    @abstractmethod
    def left_click(self) -> None: ...

    @abstractmethod
    def right_click(self) -> None: ...

    @abstractmethod
    def middle_click(self) -> None: ...

    @abstractmethod
    def press_button(self, button: str) -> None: ...
