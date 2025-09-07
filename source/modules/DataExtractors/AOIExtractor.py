from typing import Any, List, Tuple
from source.enums.DetectedObject import DetectedObject
from source.helpers.TryParse import try_parse
from source.modules.DataExtractors.BaseDataExtractor import BaseDataExtractor
from PIL import Image
import cv2
import numpy as np
import source.config as cfg
from source.transporter.Bbox import Bbox
from source.transporter.event.DataExtracted import DataExtracted


class AOIExtractor(BaseDataExtractor):
    prev_boxes: List[Tuple[int, int, int, int]] = []

    def __init__(self):
        super().__init__()
        self.config = self.config.get(cfg.CFG_KEY_AOIEXTRACTOR)

    def process_data(self, data: Any) -> DataExtracted:
        if isinstance(data, Image.Image):
            return self.extract_data_from_pil_image(data)
        else:
            raise NotImplementedError

    def extract_data_from_pil_image(self, img: Image.Image) -> DataExtracted:
        # TODO implement the solid boxes addition and cleaning per execution of this function
        # TODO implement parametrisable colors to look after (or at least hardcode types, and parametrise color themselves)
        # TODO generalise to detect salvage, tmats, and exclude any unwanted objects

        # convert pil image to BGR image
        bgr_image = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

        hsv = [((20, 100, 150), (90, 255, 255))]
        # hsv = [((45, 100, 150), (75, 255, 255))]
        # lab = [((160, 108, 198), (250, 148, 228))]
        # lab = [((198, 108, 198), (250, 148, 228))]
        # lab = [((65, 120, 198), (100, 138, 255))]

        mask = self.__build_color_mask(bgr_image, hsv_ranges=hsv)

        boxes = self.__select_rois_from_mask(
            mask, aspect_min=0.4, aspect_max=2.5, solidity_min=0
        )
        max_boxes = try_parse(self.config.get("max_salvage_output"), int, -1)
        max_memory = try_parse(self.config.get("max_boxes_iteration_memory"), int, 0)
        if max_boxes < 0:
            max_boxes = 0
        if max_memory < 0:
            max_memory = 0

        if max_boxes > 0:
            boxes = boxes[:max_boxes]
        self.__add_to_prev_boxes(boxes, max_boxes, max_memory)

        if self.config.get("save_images_with_detections"):
            self.__save_images_with_detections(bgr_image, boxes, mask, img.size)

        data = {}
        if boxes:
            data[DetectedObject.Salvage] = [
                {"box": Bbox(*x), "box_relative": Bbox(*x).to_relative(img.size)}
                for x in boxes
            ]

        return DataExtracted(data=data)

    def __add_to_prev_boxes(
        self, boxes: List[Tuple[int, int, int, int]], max_boxes: int, max_memory
    ) -> None:
        self.prev_boxes.extend(boxes)
        while len(self.prev_boxes) > max_boxes * max_memory:
            self.prev_boxes.pop(0)

    def __save_images_with_detections(
        self, bgr_image, boxes, mask, img_size: Tuple[int, int]
    ) -> None:
        import os
        import time
        from source.helpers.Params import read_params

        max_boxes = try_parse(self.config.get("max_salvage_output"), int, -1)
        if max_boxes < 0:
            max_boxes = 0
        if max_boxes:
            boxes = boxes[:max_boxes]

        scroop_ref_point = (
            read_params().get("Scrooper", {}).get("refference_point", [0, 0])
        )
        scroop_ref_point = [
            int(scroop_ref_point[0] * img_size[0]),
            int(scroop_ref_point[1] * img_size[1]),
        ]

        for cnt, (x, y, w, h) in enumerate(boxes):  # choose top-k
            cv2.rectangle(bgr_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(
                bgr_image,
                f"det_{cnt}",
                (x, y),
                cv2.FONT_HERSHEY_COMPLEX_SMALL,
                1,
                (0, 0, 0),
            )
        cv2.circle(bgr_image, scroop_ref_point, 5, (255, 0, 0, 255), 5)

        cv2.imwrite(
            os.path.join(cfg.DEV_TEST_IMAGE, f"test_output_{int(time.time())}.jpg"),
            bgr_image,
        )
        cv2.imwrite(
            os.path.join(cfg.DEV_TEST_IMAGE, f"mask_{int(time.time())}.jpg"), mask
        )

    def __build_color_mask(
        self,
        bgr_img: np.ndarray,
        hsv_ranges: List[Tuple[Tuple[int, int, int], Tuple[int, int, int]]] = [],
        lab_ranges: List[Tuple[Tuple[int, int, int], Tuple[int, int, int]]] = [],
    ) -> np.ndarray:
        hsv = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)
        mask = np.zeros(hsv.shape[:2], dtype=np.uint8)

        if hsv_ranges:
            for lo, hi in hsv_ranges:
                mask |= cv2.inRange(
                    hsv, np.array(lo, dtype=np.uint8), np.array(hi, dtype=np.uint8)
                )

        if lab_ranges:
            lab = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2LAB)
            for lo, hi in lab_ranges:
                mask |= cv2.inRange(
                    lab, np.array(lo, dtype=np.uint8), np.array(hi, dtype=np.uint8)
                )

        # Clean-up
        mask = cv2.morphologyEx(
            mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=1
        )
        mask = cv2.morphologyEx(
            mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8), iterations=2
        )
        return mask

    def __select_rois_from_mask(
        self,
        mask: np.ndarray,
        *,
        min_area: int = 200,
        max_area: int = 200000,
        aspect_min: float = 0.2,
        aspect_max: float = 5.0,
        solidity_min: float = 0.80,
        pad: int = 6,
        include_rects: List[
            Tuple[int, int, int, int]
        ] = [],  # [(x,y,w,h), ...] treated as allowed zones
        exclude_rects: List[
            Tuple[int, int, int, int]
        ] = [],  # [(x,y,w,h), ...] areas to ignore
    ) -> List[Tuple[int, int, int, int]]:
        h, w = mask.shape

        # Include/exclude given regions in/from the mask
        roi_mask = np.ones_like(mask, dtype=np.uint8) * 255
        if include_rects:
            roi_mask[:] = 0
            for x, y, ww, hh in include_rects:
                cv2.rectangle(roi_mask, (x, y), (x + ww, y + hh), 255, -1)
        if exclude_rects:
            for x, y, ww, hh in exclude_rects:
                cv2.rectangle(roi_mask, (x, y), (x + ww, y + hh), 0, -1)

        mask = cv2.bitwise_and(mask, roi_mask)

        # find all candidates, excluding those that don't match given parameters
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        candidates = []
        for c in contours:
            area = cv2.contourArea(c)
            if area < min_area or area > max_area:
                continue
            x, y, ww, hh = cv2.boundingRect(c)
            aspect = ww / float(hh)
            if aspect < aspect_min or aspect > aspect_max:
                continue
            # find a polygon that includes this contour
            hull = cv2.convexHull(c)
            hull_area = cv2.contourArea(hull) + 1e-6
            solidity = area / hull_area
            if solidity < solidity_min:
                continue

            # pad & clamp
            x0 = max(0, x - pad)
            y0 = max(0, y - pad)
            x1 = min(w, x + ww + pad)
            y1 = min(h, y + hh + pad)
            cx, cy = x + ww / 2.0, y + hh / 2.0
            candidates.append(((x0, y0, x1 - x0, y1 - y0), area, (cx, cy)))

        def score(entry):
            (x, y, ww, hh), area, (cx, cy) = entry
            s = area  # base: larger blobs first
            if self.prev_boxes:  # temporal boost: prefer near previous AOIs
                d = min(
                    ((cx - (px + pw / 2)) ** 2 + (cy - (py + ph / 2)) ** 2) ** 0.5
                    for (px, py, pw, ph) in self.prev_boxes
                )
                s += max(0, 10000 - d)  # tune the 10000 to your scale
            # mild center preference (optional)
            s += 0.001 * ((w / 2 - cx) ** 2 + (h / 2 - cy) ** 2) * -1
            return s

        candidates.sort(key=score, reverse=True)
        return [c[0] for c in candidates]  # [(x,y,w,h), ...]
