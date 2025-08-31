from source.modules.DataExtractors.BaseDataExtractor import BaseDataExtractor
from PIL import Image


class MovingWindowScanner(BaseDataExtractor):
    def process_data(self, data):
        # check if data is a PIL.Image.Image
        if not isinstance(data, Image.Image):
            img = self.try_parse_to_PILImage(data)
        else:
            img = data
