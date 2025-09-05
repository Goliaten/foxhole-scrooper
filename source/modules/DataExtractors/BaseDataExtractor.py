from abc import abstractmethod
from typing import Any
from source.modules.BaseModule import BaseModule
from PIL import Image

from source.transporter.event.Event import Event


class BaseDataExtractor(BaseModule):
    """
    For extracting useful data from an image, and converting it to usable format.
    """

    @abstractmethod
    def process_data(self, data: Any) -> Event: ...

    @abstractmethod
    def extract_data_from_pil_image(self, img: Image.Image) -> Event: ...
