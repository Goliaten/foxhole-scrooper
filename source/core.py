from source.modules.DataExtractors.AOIExtractor import AOIExtractor
from source.modules.DataProcessors.Scrooper import Scrooper
from source.modules.ImageAcquirers.MSSImageAcquirer import MSSImageAcquirer


class Core:
    # _instance: "Core"

    # def __call__(cls, *args, **kwargs):
    #     if cls not in cls._instances:
    #         cls._instances = super(Core, cls).__call__(*args, **kwargs)
    #     return cls._instances
    def __init__(self):
        self.ss_taker = MSSImageAcquirer()

    def run(self):
        run_condition = True

        while run_condition:
            raise NotImplementedError
            # get image from screen
            # process the image
            # extract the data
            # process the data
            # pass data to movement controller
            # repeat

    def dev(self):
        import time
        from PIL import Image
        import os
        import source.config as cfg
        from source.modules.DataExtractors.dev_ColorDetector import ColorDetector

        def avg(lst):
            if not lst:
                return 0
            return sum(lst) / len(lst)

        times_100 = []
        times_100_img = []
        times_100_aoi = []
        times_100_scrooper = []
        while True:
            time.sleep(1)
            t0 = time.time_ns()
            img = MSSImageAcquirer().take_screenshot()
            t1a = time.time_ns()
            event = AOIExtractor().extract_data_from_pil_image(img)
            t1b = time.time_ns()
            Scrooper().process_data(event)
            t1 = time.time_ns()

            times_100.append(t1 - t0)
            times_100_img.append(t1a - t0)
            times_100_aoi.append(t1b - t1a)
            times_100_scrooper.append(t1 - t1b)

            while len(times_100_img) > 100:
                times_100_img.pop(0)
            while len(times_100_aoi) > 100:
                times_100_aoi.pop(0)
            while len(times_100_scrooper) > 100:
                times_100_scrooper.pop(0)
            while len(times_100) > 100:
                times_100.pop(0)
            print(
                f"Total: {round(avg(times_100) / 1e9, 6)}s; "
                f"Image: {round(avg(times_100_img) / 1e9, 6)}s; "
                f"AOI: {round(avg(times_100_aoi) / 1e9, 6)}s; "
                f"Scrooper: {round(avg(times_100_scrooper) / 1e9, 6)}s"
            )
        exit()

        while True:
            time.sleep(1)


def main() -> None:
    Core().dev()
    Core().run()

    exit()
