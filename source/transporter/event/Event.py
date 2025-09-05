from dataclasses import dataclass, field
import time
from typing import Any, Dict

from source.enums.EventTypes import EventTypes


@dataclass
class Event:
    type: EventTypes = EventTypes.Generic
    timestamp: float = field(default_factory=time.time)
    data: Dict[str, Any] = field(default_factory=dict)
