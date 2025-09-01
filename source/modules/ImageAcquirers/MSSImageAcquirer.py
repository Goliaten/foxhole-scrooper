from source.modules.screenshot_takers.BaseScreenshotTaker import BaseScreenshotTaker
import mss
from PIL import Image


class MSSScreenshotTaker(BaseScreenshotTaker):
    def take_screenshot(self) -> Image.Image:
        with mss.mss() as sct:
            try:
                mon = sct.monitors[
                    int(self.config.get("ScreenshotTaker", {}).get("monitor_number", 1))
                ]
            except IndexError:
                print(
                    f"Invalid monitor index (`monitor_number` parameter). Allowed range is <0,{len(sct.monitors) - 1}>"
                )
                exit(1)
            sct_img = sct.grab(mon)

            img = Image.new("RGB", sct_img.size)
            pixels = zip(sct_img.raw[2::4], sct_img.raw[1::4], sct_img.raw[::4])
            img.putdata(list(pixels))

            return img
