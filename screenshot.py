from PIL import Image, ImageGrab
import cv2
import numpy
import os

class Screenshot:
    def __init__(self, 
                 bbox: tuple[int, int, int, int],
                 HUD_size: int,
                 threshold: int,
                 icons_name: list[str]):
        self.bbox = bbox
        self.threshold = threshold
        self.buffs = {}
   
        for buff in icons_name:
            images = []
            for filename in os.listdir(f'data/detection/{buff}/{HUD_size}/'):
                images.append(Image.open(f'data/detection/{buff}/{HUD_size}/{filename}').convert('L'))
            self.buffs[buff] = images

    def refresh(self):
        """
        Return tuple of milliseconds till next update and string message to display
        """
        # ScreenShot
        screen_image = ImageGrab.grab(bbox=self.bbox)
        pil_data = screen_image.convert('L')
        screen_image = numpy.array(pil_data)

        detectedBuffs = {}
        # Iterate over Buffs to detect
        for buff, images in self.buffs.items():
            detectedBuffs[buff] = False
            for image in images:
                np_image = numpy.array(image)
                result = self.is_template_in_image(np_image, screen_image)
                if result == True:
                    detectedBuffs[buff] = True
                    break

        return detectedBuffs

    def is_template_in_image(self, buff, global_image) -> bool:
        """
        Detect if buff is in global_image
        """
        result = cv2.matchTemplate(global_image, buff, cv2.TM_SQDIFF)
        (yCoords, xCoords) = numpy.where(result <= self.threshold)
        return yCoords.size > 0
