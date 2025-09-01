from source.modules.DataExtractors.BaseDataExtractor import BaseDataExtractor
from PIL import Image


class MovingWindowScanner(BaseDataExtractor):
    def process_data(self, data):
        # check if data is a PIL.Image.Image
        if not isinstance(data, Image.Image):
            img = self.try_parse_to_PILImage(data)
        else:
            img = data  # noqa: F841

    def extract_data_from_pil_image(self, img: Image.Image) -> None:
        raise NotImplementedError
