from abc import abstractmethod
from source.modules.BaseModule import BaseModule


class BaseMovementController(BaseModule):
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
