
from typing import Iterable, List, Tuple
from source.enums.DetectedObject import DetectedObject
from source.enums.EventTypes import EventTypes
from source.modules.DataProcessors.BaseDataProcessor import BaseDataProcessor
from source.transporter.event.DataExtracted import DataExtracted
from source.transporter.event.Event import Event
from source.typed_dicts.DetectedObjectInstance import DetectedObjectInstance
import config as cfg

# TODO act if inventory is full
# TODO act if field is empty
class Scrooper(BaseDataProcessor):

    def __init__(self):
        super().__init__()
        self.config = self.config.get(cfg.CFG_KEY_SCROOPER)

    def process_data(self, event: Event) -> Event:
        
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

        return None
    
    def scroop_tmat(self, data: List[DetectedObjectInstance]) -> Event:
        raise NotImplementedError

    def scroop(self, data: List[DetectedObjectInstance]) -> Event:
        # check where is the bbox
        # ? check if it's large enough
        ref_point =self.get_refference_point()

        for det_object in data:
            if not self.check_detected_object_instance(det_object):
                continue

        else:
            # TODO send a message into process_extracted_data, that no tmat was succesfully processed
            pass

        # rotate camera
        # move towards tmat
        # gather it if it's close enough
        return None

    def check_detected_object_instance(self, inp: DetectedObjectInstance) -> True:
        return True
    
    def get_refference_point(self) -> Tuple[int, int]:
        ref_point: Tuple[float, float] = self.config.get("refference_point", ())
        if not ref_point or not isinstance(ref_point, Iterable) or not len(ref_point) == 2:
            raise ValueError("Expected `[Scrooper].refference_point` parameter to be an iterable with length of 2.")
        
        # FIXME hardcoded screen resolution
        screen_x, screen_y = 1920,1080

        out = (ref_point[0]*screen_x, ref_point[1]*screen_y)

        return out