from source.helpers.OffsetPoint import offset_point_provided_config
from source.modules.BaseModule import BaseModule
import pyautogui as pg


class ClickCenter(BaseModule):
    """Debug movement controller, meant to click on center of screen"""

    def click_on_center(self):
        screen = pg.size()
        point = int(screen[0] / 2), int(screen[1] / 2)
        point = offset_point_provided_config(point, self.config)
        print(point)
        pg.moveTo(point)
