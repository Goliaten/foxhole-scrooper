from abc import abstractmethod
from source.modules.BaseModule import BaseModule
from source.transporter.event.Event import Event


class BaseDataProcessor(BaseModule):
    """
    For parsing data extracted from image, and deciding what to do.
    """

    @abstractmethod
    def process_data(self, data: Event) -> Event: ...
