import os
from typing import Any, List, Tuple
from source.modules.DataExtractors.BaseDataExtractor import BaseDataExtractor
from PIL import Image
import cv2
import numpy as np
import source.config as cfg


class AOIExtractor(BaseDataExtractor):
    def process_data(self, data):
        raise NotImplementedError

    def extract_data_from_pil_image(self, img: Image.Image) -> Any:
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

        for x, y, w, h in boxes[:5]:  # choose top-k
            cv2.rectangle(bgr_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imwrite(os.path.join(cfg.DEV_TEST_IMAGE, "test_output.jpg"), bgr_image)
        cv2.imwrite(os.path.join(cfg.DEV_TEST_IMAGE, "mask.jpg"), mask)

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
        min_area=200,
        max_area=200000,
        aspect_min=0.2,
        aspect_max=5.0,
        solidity_min=0.80,
        pad=6,
        include_rects: List[
            Tuple[int, int, int, int]
        ] = None,  # [(x,y,w,h), ...] treated as allowed zones
        exclude_rects: List[
            Tuple[int, int, int, int]
        ] = None,  # [(x,y,w,h), ...] areas to ignore
        prev_boxes=None,
    ):
        # TODO comprehend
        h, w = mask.shape
        roi_mask = np.ones_like(mask, dtype=np.uint8) * 255
        if include_rects:
            roi_mask[:] = 0
            for x, y, ww, hh in include_rects:
                cv2.rectangle(roi_mask, (x, y), (x + ww, y + hh), 255, -1)
        if exclude_rects:
            for x, y, ww, hh in exclude_rects:
                cv2.rectangle(roi_mask, (x, y), (x + ww, y + hh), 0, -1)

        mask = cv2.bitwise_and(mask, roi_mask)

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
            if prev_boxes:  # temporal boost: prefer near previous AOIs
                d = min(
                    ((cx - (px + pw / 2)) ** 2 + (cy - (py + ph / 2)) ** 2) ** 0.5
                    for (px, py, pw, ph) in prev_boxes
                )
                s += max(0, 10000 - d)  # tune the 10000 to your scale
            # mild center preference (optional)
            s += 0.001 * ((w / 2 - cx) ** 2 + (h / 2 - cy) ** 2) * -1
            return s

        candidates.sort(key=score, reverse=True)
        return [c[0] for c in candidates]  # [(x,y,w,h), ...]
