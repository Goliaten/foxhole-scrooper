from dataclasses import dataclass

from source.transporter.MovementControllerInputs.BaseMovementControllerInput import (
    BaseMovementControllerInput,
)


@dataclass(frozen=True)
class WalkTransporter(BaseMovementControllerInput):
    period: float
