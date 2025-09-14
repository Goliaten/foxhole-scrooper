from dataclasses import dataclass, field
import time
from typing import Any, Dict

from source.enums.EventTypes import EventTypes
from source.enums.MovementActions import MovementActions
from source.transporter.MovementControllerInputs.BaseMovementControllerInput import (
    BaseMovementControllerInput,
)
from source.transporter.event.Event import Event


@dataclass(frozen=True)
class DataProcessed(Event):
    type: EventTypes = EventTypes.DataProcessed
    timestamp: float = field(default_factory=time.time)
    data: Dict[MovementActions, BaseMovementControllerInput] = field(
        default_factory=dict
    )
