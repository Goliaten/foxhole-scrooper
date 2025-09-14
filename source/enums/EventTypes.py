from enum import Enum


class EventTypes(Enum):
    Empty = "EMPTY"
    Generic = "GENERIC"
    ImageDetected = "IMAGE_DETECTED"
    ImageProcessed = "IMAGE_PROCESSED"
    DataExtracted = "DATA_EXTRACTED"
    DataProcessed = "DATA_PROCESSED"
