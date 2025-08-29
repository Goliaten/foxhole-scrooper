from abc import abstractmethod
from PIL.Image import Image
from source.modules.BaseModule import BaseModule


class BaseScreenshotTaker(BaseModule):
    @abstractmethod
    def take_screenshot(self) -> Image: ...
