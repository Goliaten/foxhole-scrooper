import win32api
import threading
import time

from source.helpers.OffsetPoint import offset_point_provided_config
from source.helpers.Params import read_params


def start_click_listener():
    th1 = threading.Thread(target=click_listener, daemon=True)
    th1.start()


def click_listener():
    # https://stackoverflow.com/a/41930485
    config = read_params()
    state_left = win32api.GetKeyState(
        0x01
    )  # Left button down = 0 or 1. Button up = -127 or -128
    state_right = win32api.GetKeyState(
        0x02
    )  # Right button down = 0 or 1. Button up = -127 or -128

    while True:
        a = win32api.GetKeyState(0x01)
        b = win32api.GetKeyState(0x02)

        if a != state_left:  # Button state changed
            state_left = a
            pos = win32api.GetCursorPos()
            print(
                f"original: {pos} offset: {offset_point_provided_config(pos, config, reverse=True)}"
            )

        if b != state_right:  # Button state changed
            state_right = b
            pos = win32api.GetCursorPos()
            print(
                f"original: {pos} offset: {offset_point_provided_config(pos, config, reverse=True)}"
            )

        time.sleep(0.001)
