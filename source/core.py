from source.modules.screenshot_takers.MSSScreenshotTaker import MSSScreenshotTaker


class Core:
    # _instance: "Core"

    # def __call__(cls, *args, **kwargs):
    #     if cls not in cls._instances:
    #         cls._instances = super(Core, cls).__call__(*args, **kwargs)
    #     return cls._instances
    def __init__(self):
        self.ss_taker = MSSScreenshotTaker()

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


def main() -> None:
    Core().run()

    exit()
