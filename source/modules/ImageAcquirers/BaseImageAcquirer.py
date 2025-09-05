from abc import abstractmethod
from PIL.Image import Image
from source.modules.BaseModule import BaseModule


class BaseImageAcquirer(BaseModule):
    """
    For acquiring images.
    """

    @abstractmethod
    def take_screenshot(self) -> Image: ...
