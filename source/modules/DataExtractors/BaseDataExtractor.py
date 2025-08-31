from abc import abstractmethod
from typing import Any
from source.modules.BaseModule import BaseModule


class BaseDataExtractor(BaseModule):
    @abstractmethod
    def process_data(self, data: Any) -> Any: ...
