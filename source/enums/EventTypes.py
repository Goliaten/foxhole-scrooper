from enum import Enum


class EventTypes(Enum):
    Generic = "GENERIC"
    ImageDetected = "IMAGE_DETECTED"
    ImageProcessed = "IMAGE_PROCESSED"
