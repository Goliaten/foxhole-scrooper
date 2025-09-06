from dataclasses import dataclass, field
from typing import Dict, List
from source.enums.DetectedObject import DetectedObject
from source.transporter.event.Event import Event
from source.enums.EventTypes import EventTypes
from source.typed_dicts.DetectedObjectInstance import DetectedObjectInstance


@dataclass(frozen=True)
class DataExtracted(Event):
    type: EventTypes = EventTypes.DataExtracted
    data: Dict[DetectedObject, List[DetectedObjectInstance]] = field(
        default_factory=dict
    )  # type: ignore
