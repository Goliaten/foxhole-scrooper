from abc import abstractmethod

import toml
from source.enums.MovementActions import MovementActions
from source.modules.BaseModule import BaseModule
import source.config as cfg
from source.transporter.MovementControllerInputs.ClickTransporter import (
    ClickTransporter,
)
from source.transporter.MovementControllerInputs.RotateTransporter import (
    RotateTransporter,
)
from source.transporter.MovementControllerInputs.WalkTransporter import WalkTransporter
from source.transporter.event.DataProcessed import DataProcessed
from source.transporter.event.Event import Event


class BaseMovementController(BaseModule):
    """
    For controlling the game.
    """

    def __init__(self):
        super().__init__()
        with open(cfg.LOCATIONS_PATH, "r") as file:
            self.locations = toml.load(file)
        self.config = self.config.get(cfg.CFG_KEY_MOVEMENT_CONTROLLER)

    def act_on_event(self, event: Event) -> None:
        if not isinstance(event, DataProcessed):
            print(
                f"Wrong event class for movement controller. Expected `DataProcessed` got {type(event)}"
            )
            return

        print("Got DataProcessed event")
        # NOTE although I expect only one action to be in one event, i'll handle several actions here.
        for key, value in event.data.items():
            print(f"got some {key=} and {value=}")
            match key:
                case MovementActions.ClickLeft:
                    assert isinstance(value, ClickTransporter)
                    print(f"Action: Left Click {value=}")
                    if not self.config.get("dry_run"):
                        self.left_click()
                case MovementActions.WalkUp:
                    assert isinstance(value, WalkTransporter)
                    print(f"Action: Walk Up {value=}")
                    if not self.config.get("dry_run"):
                        self.walk_up(value.period)
                case MovementActions.RotateLeft:
                    assert isinstance(value, RotateTransporter)
                    print(f"Action: Rotate Left {value=}")
                    if not self.config.get("dry_run"):
                        self.rotate_left(value.period)
                case MovementActions.RotateRight:
                    assert isinstance(value, RotateTransporter)
                    print(f"Action: Rotate Right {value=}")
                    if not self.config.get("dry_run"):
                        self.rotate_right(value.period)
            # TODO implement the other actions

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

    # TODO implement click_center function from puautogui MC here in generalised form
