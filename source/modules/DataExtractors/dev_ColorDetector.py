import time
from source.modules.DataExtractors.BaseDataExtractor import BaseDataExtractor
from PIL import Image
from colorama import just_fix_windows_console

just_fix_windows_console()


class ColorDetector(BaseDataExtractor):
    def process_data(self, data):
        # check if data is a PIL.Image.Image
        # count all colors on it, and time it
        # try a sparse check
        # print out all colors using anssi escape sequence

        if not isinstance(data, Image.Image):
            img = self.try_parse_to_PILImage(data)
        else:
            img = data

        # sparse_x = 1
        # sparse_y = 1
        results = {}
        for sparse_x in range(1, 11):
            for sparse_y in range(1, 11):
                colors = {}
                print(f"{sparse_x=} {sparse_y=}")
                t0 = time.time_ns()
                for x in range(0, img.size[0], sparse_x):
                    for y in range(0, img.size[1], sparse_y):
                        pixel = img.getpixel((x, y))
                        if pixel in colors:
                            colors[pixel] += 1
                        else:
                            colors[pixel] = 1
                t1 = time.time_ns()
                results[(sparse_x, sparse_y)] = int((t1 - t0) / 10e3)

        # print(results)
        print("Results of checking every nth pixel on 1920x1080 image.")
        print("Values in microseconds")
        for x in range(1, 11):
            for y in range(1, 11):
                print(f"({x},{y})={results[(x, y)]}", end="; ")
            print()

        pixels, items = list(colors.keys()), list(colors.values())
        items, pixels = zip(*sorted(zip(items, pixels), reverse=True))
        for pixel, cnt in zip(pixels[:20], items[:20]):
            print(
                f"\033[38;2;{pixel[0]};{pixel[1]};{pixel[2]}m█\033[0m {pixel} - {cnt} count"
            )

    def extract_data_from_pil_image(self, img):
        raise NotImplementedError
