import configparser

from overlay import Overlay
from screenshot import Screenshot


def main() -> None:

    config = configparser.ConfigParser()
    config.read('config.ini')

    buff_names = []
    for key in config['Buffs']:
        if config['Buffs'].getboolean(key):
            buff_names.append(key)
    debuff_names = []
    for key in config['Debuffs']:
        if config['Debuffs'].getboolean(key):
            debuff_names.append(key)

    hud_size = config['TL'].getint('HUD_size')
    screenshot_width = config['TL'].getint('width')
    screenshot_height = config['TL'].getint('height')

    screenshot_buff_left_x = config['TL.Buff'].getint('left_X')
    screenshot_buff_top_y = config['TL.Buff'].getint('top_Y')

    screenshot_debuff_left_x = config['TL.Debuff'].getint('left_X')
    screenshot_debuff_top_y = config['TL.Debuff'].getint('top_Y')

    initial_delay = config['Settings'].getint('initial_delay')
    refresh_rate = config['Settings'].getint('refresh_rate')
    threshold = config['Settings'].getfloat('threshold')

    icon_size = config['Overlay'].getint('icon_size')
    overlay_left_x = config['Overlay'].getint('left_X')
    overlay_top_y = config['Overlay'].getint('top_Y')
    horizontal = config['Overlay'].getboolean('horizontal')

    buffs = Screenshot(
        bbox=(screenshot_buff_left_x, screenshot_buff_top_y, screenshot_buff_left_x+screenshot_width, screenshot_buff_top_y+screenshot_height),
        hud_size=hud_size,
        threshold=threshold,
        icons_name=buff_names,
        )

    debuffs = Screenshot(
        bbox=(screenshot_debuff_left_x, screenshot_debuff_top_y, screenshot_debuff_left_x+screenshot_width, screenshot_debuff_top_y+screenshot_height),
        hud_size=hud_size,
        threshold=threshold,
        icons_name=debuff_names,
        )

    overlay = Overlay(
        initial_delay=initial_delay,
        refresh_rate=refresh_rate,
        get_buffs_status=buffs.refresh,
        get_debuffs_status=debuffs.refresh,
        buffs_names=buff_names,
        debuffs_names=debuff_names,
        geometry=(overlay_left_x, overlay_top_y),
        icon_size=icon_size,
        horizontal=horizontal
        )
    overlay.run()

if __name__ == '__main__':
    main()
