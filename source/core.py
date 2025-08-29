import os
import toml

from source.helpers.Singleton import Singleton


class Core(metaclass=Singleton):
    # _instance: "Core"

    # def __call__(cls, *args, **kwargs):
    #     if cls not in cls._instances:
    #         cls._instances = super(Core, cls).__call__(*args, **kwargs)
    #     return cls._instances
    def __init__(self):
        pass

    def run(self):
        run_condition = True

        while run_condition:
            pass
            # get image from screen
            # process the image
            # extract the data
            # pass data to movement controller
            # repeat


def main() -> None:
    params = toml.load(os.path.join("params.toml"))
    # TODO don't start these subprocesses if we run position spew or screenshot check

    Core().run()

    exit()
    # raise NotImplementedError
    # try:
    #     ...
    # except SystemExit:
    #     pass
    # except BaseException:
    #     traceback.print_exc()
