import math
from typing import Iterable, List, Literal, Tuple
from source.enums.DetectedObject import DetectedObject
from source.enums.EventTypes import EventTypes
from source.modules.DataProcessors.BaseDataProcessor import BaseDataProcessor
from source.transporter.event.DataExtracted import DataExtracted
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

    def process_data(self, event: Event) -> Event:
        out = Event(type=EventTypes.Empty)

        if event.type == EventTypes.DataExtracted:
            assert isinstance(event, DataExtracted)
            out = self.process_extracted_data(event)

        return out

    def process_extracted_data(self, event: DataExtracted) -> Event:
        assert isinstance(event, DataExtracted)

        if DetectedObject.TechMaterial in event.data:
            print("got tmat detected")
            self.scroop_tmat(event.data[DetectedObject.TechMaterial])
        elif DetectedObject.Salvage in event.data:
            print("got salvage detected")
            self.scroop(event.data[DetectedObject.Salvage])

        return Event(type=EventTypes.Empty)

    def scroop_tmat(self, data: List[DetectedObjectInstance]) -> Event:
        raise NotImplementedError

    def scroop(self, data: List[DetectedObjectInstance]) -> Event:
        # check where is the bbox
        # ? check if it's large enough
        ref_point = self.get_refference_point(scale=True)
        top_point_scaled = (ref_point[0], 0)
        front_angle = 10  # FIXME hardoced param
        close_dist = 50  # FIXME hardoced param
        very_close_dist = 20  # FIXME hardoced param

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

            # TODO if player is in front of it - gather it
            if abs(angle) < front_angle and dist <= close_dist:
                print(f"gather salvage (close enough) {dist=} {angle=}")

            # TODO if object is in center above player - move towards tmat
            if abs(angle) <= front_angle:
                print(f"move by {dist} {dist=} {angle=}")

            # TODO if object is at off angle - rotate camera
            if abs(angle) > front_angle:
                direction = math.copysign(1, angle)
                print(f"rotate {direction} by {abs(angle)} {dist=} {angle=}")

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
