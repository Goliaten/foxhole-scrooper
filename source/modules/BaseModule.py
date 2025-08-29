from typing import Any, Dict
import toml

from source.helpers.Singleton import Singleton
import source.config as cfg


class BaseModule(metaclass=Singleton):
    config: Dict[str, Any]

    def __init__(self) -> None:
        self.config = self.read_params()

    @staticmethod
    def read_params() -> Dict[str, Any]:
        with open(cfg.PARAMS_PATH, "r") as file:
            return toml.load(file)
