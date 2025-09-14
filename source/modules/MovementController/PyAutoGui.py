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
    def walk_up(self, period: float):
        self.__press_key_for_time("w", period)

    def walk_right(self, period: float):
        self.__press_key_for_time("d", period)

    def walk_left(self, period: float):
        self.__press_key_for_time("a", period)

    def walk_down(self, period: float):
        self.__press_key_for_time("s", period)

    def rotate_right(self, period: float):
        self.__press_key_for_time(".", period)

    def rotate_left(self, period: float):
        self.__press_key_for_time(",", period)

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
