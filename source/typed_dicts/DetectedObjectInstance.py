from typing import TypedDict
from source.transporter.Bbox import Bbox


class DetectedObjectInstance(TypedDict):
    box: Bbox
    box_relative: Bbox
