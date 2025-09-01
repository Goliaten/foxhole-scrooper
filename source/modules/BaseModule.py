from abc import ABC
from typing import Any, Dict

from source.helpers.Params import read_params
from source.helpers.Singleton import Singleton


class BaseModule(Singleton, ABC):
    config: Dict[str, Any]

    def __init__(self) -> None:
        self.config = read_params()
