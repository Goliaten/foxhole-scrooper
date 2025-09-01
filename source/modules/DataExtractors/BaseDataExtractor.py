from abc import abstractmethod
from typing import Any
from source.modules.BaseModule import BaseModule
from PIL import Image


class BaseDataExtractor(BaseModule):
    @abstractmethod
    def process_data(self, data: Any) -> Any: ...

    @abstractmethod
    def extract_data_from_pil_image(self, img: Image.Image) -> Any: ...
