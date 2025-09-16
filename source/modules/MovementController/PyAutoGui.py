from source.helpers.OffsetPoint import offset_point, offset_point_provided_config
from source.modules.MovementController.BaseMovementController import (
    BaseMovementController,
)
import time

try:
    import pyautogui as pg
except Exception as e:
    print("""Couldn't import `pyautogui` module for PyAutoGui movement controller.
          Make sure this module is installed globally or in your venv.""")
    raise e


class PyAutoGui(BaseMovementController):
    clicked_center = False

    def __init__(self):
        super().__init__()
        self.__click_center()

    def walk_up(self, period: float):
        self.__press_key_for_time("w", period)

    def walk_right(self, period: float):
        self.__press_key_for_time("d", period)

    def walk_left(self, period: float):
        self.__press_key_for_time("a", period)

    def walk_down(self, period: float):
        self.__press_key_for_time("s", period)

    def rotate_right(self, period: float):
        self.__press_key_for_time(",", period)

    def rotate_left(self, period: float):
        self.__press_key_for_time(".", period)

    def left_click(self):
        pg.leftClick()

    def right_click(self):
        pg.rightClick()

    def middle_click(self):
        pg.middleClick()

    def press_button(self, button: str):
        pg.typewrite([button])

    def __press_key_for_time(self, key: str, period: float):
        pg.keyDown(key)
        time.sleep(period)
        pg.keyUp(key)

    def __click_center(self):
        if PyAutoGui.clicked_center:
            return

        PyAutoGui.clicked_center = True
        screen = pg.size()
        point = self.config.get("center_click_pos")
        point = int(screen[0] * point[0]), int(screen[1] * point[1])
        # point = int(screen[0] / 2), int(screen[1] / 2)
        off_x = self.config.get("offset_x")
        off_y = self.config.get("offset_y")
        point = offset_point(point, (off_x, off_y))
        print(point)
        pg.moveTo(point)
        pg.middleClick()
