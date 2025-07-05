import os

import cv2
import numpy
from PIL import Image, ImageGrab


class Screenshot:
    def __init__(self,
                 bbox: tuple[int, int, int, int],
                 hud_size: int,
                 threshold: float,
                 icons_name: list[str]):
        self.bbox = bbox
        self.threshold = threshold
        self.buffs = {}

        for buff in icons_name:
            images = []
            for filename in os.listdir(f'data/detection/{buff}/{hud_size}/'):
                images.append(Image.open(f'data/detection/{buff}/{hud_size}/{filename}').convert('L'))
            self.buffs[buff] = images

    def refresh(self):
        """
        Return tuple of milliseconds till next update and string message to display
        """
        # ScreenShot
        screen_image = ImageGrab.grab(bbox=self.bbox)
        pil_data = screen_image.convert('L')
        screen_image = numpy.array(pil_data)

        detected_buffs = {}
        # Iterate over Buffs to detect
        for buff, images in self.buffs.items():
            detected_buffs[buff] = False
            for image in images:
                np_image = numpy.array(image)
                result = self.is_template_in_image(np_image, screen_image)
                if result:
                    detected_buffs[buff] = True
                    break

        return detected_buffs

    def is_template_in_image(self, buff, global_image) -> bool:
        """
        Detect if buff is in global_image
        """
        result = cv2.matchTemplate(global_image, buff, cv2.TM_SQDIFF)
        (y, _) = numpy.where(result <= self.threshold)
        return y.size > 0
