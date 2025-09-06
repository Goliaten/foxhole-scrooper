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
            self.scroop_tmat(event.data[DetectedObject.TechMaterial])
        elif DetectedObject.Salvage in event.data:
            self.scroop(event.data[DetectedObject.TechMaterial])

        return Event(type=EventTypes.Empty)

    def scroop_tmat(self, data: List[DetectedObjectInstance]) -> Event:
        raise NotImplementedError

    def scroop(self, data: List[DetectedObjectInstance]) -> Event:
        # check where is the bbox
        # ? check if it's large enough
        ref_point = self.get_refference_point(scale=False)

        for det_object in data:
            if not self.check_detected_object_instance(det_object):
                continue
            print(
                "bingus ",
                det_object["box_relative"].get_distance_from_centers(ref_point) < 0.05,
            )

            # TODO if player is above it - gather it
            # TODO if object is in center above player - move towards tmat
            # TODO if object is at off angle - rotate camera

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
        out = (int(ref_point[0] * screen_x), int(ref_point[1] * screen_y))

        return out
