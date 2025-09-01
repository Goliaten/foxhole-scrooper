from abc import ABC, abstractmethod
from PIL.Image import Image
from source.modules.BaseModule import BaseModule


class BaseImageAcquirer(ABC, BaseModule):
    @abstractmethod
    def take_screenshot(self) -> Image: ...
