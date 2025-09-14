from source.modules.DataExtractors.AOIExtractor import AOIExtractor
from source.modules.DataProcessors.Scrooper import Scrooper
from source.modules.ImageAcquirers.MSSImageAcquirer import MSSImageAcquirer
from source.modules.MovementController.PyAutoGui import PyAutoGui


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

        PyAutoGui()
        while True:
            time.sleep(1)
            print("-------")
            img = MSSImageAcquirer().take_screenshot()
            event = AOIExtractor().extract_data_from_pil_image(img)
            event = Scrooper().process_data(event)
            PyAutoGui().act_on_event(event)
        exit()

        while True:
            time.sleep(1)


def main() -> None:
    Core().dev()
    Core().run()

    exit()
