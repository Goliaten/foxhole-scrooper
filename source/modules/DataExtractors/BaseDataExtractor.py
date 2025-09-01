from abc import ABC, abstractmethod
from typing import Any
from source.modules.BaseModule import BaseModule


class BaseDataExtractor(ABC, BaseModule):
    @abstractmethod
    def process_data(self, data: Any) -> Any: ...
