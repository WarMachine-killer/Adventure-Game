import json


def check_room_existing(x, y, tile_width, tile_height):
    if x > tile_width - 1:
        x = 0
    if y > tile_height - 1:
        y = 0
    if x < 0:
        x = tile_width - 1
    if y < 0:
        y = tile_height - 1
    return x, y


def json_read(filename):
    with open(filename,encoding="utf-8") as file:
        info = json.load(file)
        return info