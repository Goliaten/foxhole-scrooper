import os
from PIL import Image
import source.config as cfg
import random


def load_test_image(idx: int | None = None) -> Image.Image:
    """
    Picks random image from Dev/test_images directory.

    By default picks at random. Can be specified a index of which image to take.
    Idk what's the default order of os.listdir, so try and guess :P
    """
    images = os.listdir(cfg.DEV_TEST_IMAGE)
    images = [x for x in images if ".png" in x]

    if idx:
        try:
            return Image.open(os.path.join(cfg.DEV_TEST_IMAGE, images[idx]))
        except FileNotFoundError:
            print(f"Couldn't fetch file with {idx} index. Defaulting to random.")
        except IndexError:
            print(
                f"Invalid index. Found total of {len(images)} images, but received {idx} index"
            )

    return Image.open(os.path.join(cfg.DEV_TEST_IMAGE, random.choice(images)))
