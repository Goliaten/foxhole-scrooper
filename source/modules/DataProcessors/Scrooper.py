import math
from typing import Iterable, List, Literal, Tuple
from source.enums.DetectedObject import DetectedObject
from source.enums.EventTypes import EventTypes
from source.enums.MovementActions import MovementActions
from source.modules.DataProcessors.BaseDataProcessor import BaseDataProcessor
from source.transporter.MovementControllerInputs.ClickTransporter import (
    ClickTransporter,
)
from source.transporter.MovementControllerInputs.RotateTransporter import (
    RotateTransporter,
)
from source.transporter.MovementControllerInputs.WalkTransporter import WalkTransporter
from source.transporter.event.DataExtracted import DataExtracted
from source.transporter.event.DataProcessed import DataProcessed
from source.transporter.event.Event import Event
from source.typed_dicts.DetectedObjectInstance import DetectedObjectInstance
import source.config as cfg


# TODO act if inventory is full
# TODO act if field is empty
# TODO act if dead
class Scrooper(BaseDataProcessor):
    def __init__(self):
        super().__init__()
        self.config = self.config.get(cfg.CFG_KEY_SCROOPER)

    def process_data(self, event: Event) -> DataProcessed:
        out = Event(type=EventTypes.Empty)

        if event.type == EventTypes.DataExtracted:
            assert isinstance(event, DataExtracted)
            out = self.process_extracted_data(event)

        return out

    def process_extracted_data(self, event: DataExtracted) -> DataProcessed:
        assert isinstance(event, DataExtracted)

        if DetectedObject.TechMaterial in event.data:
            print("got tmat detected")
            out = self.scroop_tmat(event.data[DetectedObject.TechMaterial])
        elif DetectedObject.Salvage in event.data:
            print("got salvage detected")
            out = self.scroop(event.data[DetectedObject.Salvage])
        # TODO make default action in case there is absolutely no scroop

        return out

    def scroop_tmat(self, data: List[DetectedObjectInstance]) -> DataProcessed:
        # TODO implement scrooping TMATs
        raise NotImplementedError

    def scroop(self, data: List[DetectedObjectInstance]) -> DataProcessed:
        # check if bbox is large enough?
        ref_point = self.get_refference_point(scale=True)
        top_point_scaled = (ref_point[0], 0)
        front_angle = self.config.get("front_angle")
        close_dist = self.config.get("close_distance")
        very_close_dist = self.config.get("very_close_distance")
        medium_dist = self.config.get("medium_distance")
        medium_angle = self.config.get("medium_angle")
        rotate_time_addition = self.config.get("rotate_time_addition")
        base_walk_time = self.config.get("base_walk_time")
        distance_to_time_scale = self.config.get("distance_to_time_scale")

        data.sort(key=lambda x: x["box"].get_distance_from_centers(ref_point))

        for det_object in data:
            # FIXME enforce an order in which we check the bboxes
            if not self.check_detected_object_instance(det_object):
                continue
            dist = round(det_object["box"].get_distance_from_centers(ref_point), 3)
            angle = round(
                det_object["box"].get_angle_from_centers(ref_point, top_point_scaled), 3
            )

            # TODO if player is above it - gather it
            if dist <= very_close_dist:
                print(f"gather salvage (on top) {dist=} {angle=}")
                return DataProcessed(
                    data={MovementActions.ClickLeft: ClickTransporter()}
                )

            # TODO if player is in front of it - gather it
            if abs(angle) < front_angle and dist <= close_dist:
                print(f"gather salvage (close enough) {dist=} {angle=}")
                return DataProcessed(
                    data={MovementActions.ClickLeft: ClickTransporter()}
                )

            # TODO if object is in center above player - move towards tmat
            if abs(angle) <= front_angle:
                print(f"move (front angle) by {dist} {dist=} {angle=}")
                walk_time = base_walk_time * dist / distance_to_time_scale
                return DataProcessed(
                    data={MovementActions.WalkUp: WalkTransporter(walk_time)}
                )

            if abs(angle) < medium_angle and dist <= medium_dist:
                print(f"move (medium angle, medium dist) by {dist} {dist=} {angle=}")
                walk_time = base_walk_time * dist / distance_to_time_scale
                return DataProcessed(
                    data={MovementActions.WalkUp: WalkTransporter(walk_time)}
                )

            # TODO if object is at off angle - rotate camera
            if abs(angle) > front_angle:
                direction = math.copysign(1, angle)
                print(f"rotate {direction} by {abs(angle)} {dist=} {angle=}")
                rotate_time = (abs(angle) / 180) + rotate_time_addition

                if direction > 0:
                    return DataProcessed(
                        data={
                            MovementActions.RotateRight: RotateTransporter(rotate_time)
                        }
                    )
                else:
                    return DataProcessed(
                        data={
                            MovementActions.RotateLeft: RotateTransporter(rotate_time)
                        }
                    )

        else:
            # TODO send a message into process_extracted_data, that no tmat was succesfully processed
            pass

        return Event(type=EventTypes.Empty)

    def check_detected_object_instance(
        self, inp: DetectedObjectInstance
    ) -> Literal[True]:
        return True

    def get_refference_point(self, scale=True) -> Tuple[float, float]:
        ref_point: Tuple[float, float] = self.config.get("refference_point", ())
        if (
            not ref_point
            or not isinstance(ref_point, Iterable)
            or not len(ref_point) == 2
        ):
            raise ValueError(
                "Expected `[Scrooper].refference_point` parameter to be an iterable with length of 2."
            )
        if not scale:
            return ref_point

        # FIXME hardcoded screen resolution
        screen_x, screen_y = 1920, 1080
        out = (ref_point[0] * screen_x, ref_point[1] * screen_y)

        return out
