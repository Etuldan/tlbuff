import tkinter as tk
from typing import Callable, Any
from PIL import Image, ImageTk, ImageOps
from collections import OrderedDict

class Overlay:
    """
    Creates an overlay window using tkinter
    Uses the "-topmost" property to always stay on top of other Windows
    """
    def __init__(self,
                 initial_delay: int,
                 refresh_rate: int,
                 get_buffs_status: Callable[[], tuple[int, bool]],
                 get_debuffs_status: Callable[[], tuple[int, bool]],
                 buffsNames: list[str],
                 debuffsNames: list[str],
                 geometry: tuple[int, int],
                 icon_size: int,
                 horizontal: bool):
        self.initial_delay = initial_delay
        self.refresh_rate = refresh_rate
        self.get_buffs_status = get_buffs_status
        self.get_debuffs_status = get_debuffs_status
        self.root = tk.Tk()
        background_color = 'SteelBlue1'
        self.root.configure(background=background_color)

        self.labels=OrderedDict()
        self.images={}

        box = lambda x, y : ((x if horizontal else y), (x if not horizontal else y))

        i = 0
        for buff in buffsNames:
            self.create_icon(icon_name=buff, icon_size=icon_size, box=box(i, 0))
            i = i + 1

        i = 0
        for debuff in debuffsNames:
            self.create_icon(icon_name=debuff, icon_size=icon_size, box=box(i, 1))
            i = i + 1

        # Define Window Geometry
        self.root.overrideredirect(True)
        self.root.geometry(f'+{geometry[0]}+{geometry[1]}')
        self.root.lift()
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", background_color)

    def create_icon(self, icon_name: str, icon_size: int, box: tuple[int, int]) -> None:
        base = Image.open(f'data/render/{icon_name}.webp').resize((icon_size, icon_size))
        red = ImageOps.colorize(base.convert('L'), black='black', white='red')
        img = ImageTk.PhotoImage(base)
        imgRed = ImageTk.PhotoImage(red)
        self.images[icon_name] = [img, imgRed]
        label = tk.Label(self.root, text=icon_name, image=img, borderwidth=0, highlightthickness=0)
        x, y = box
        label.grid(row=y, column=x)
        self.labels[icon_name] = label

    def update(self) -> None:
        detectedBuffs = self.get_buffs_status()
        for buffName, detected in detectedBuffs.items():
            self.update_img(detected=detected, buff_name=buffName)

        detectedDebuffs = self.get_debuffs_status()
        for debuffName, detected in detectedDebuffs.items():
            self.update_img(detected=detected, buff_name=debuffName)

        self.root.after(self.refresh_rate, self.update)

    def update_img(self, detected: bool, buff_name: str) -> None:
        if detected:
            self.labels[buff_name].config(image=self.images[buff_name][0])
        else:
            self.labels[buff_name].config(image=self.images[buff_name][1])

    def run(self) -> None:
        self.root.after(self.initial_delay, self.update)
        self.root.mainloop()
