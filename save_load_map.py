import _json
import json


def save_map(map, x, y, room_num):
    info = {"map": map,
            "x_on_map": x,
            "y_on_map": y,
            "room_num":room_num}
    with open("map.json", "w", encoding="utf-8") as file:
        json.dump(info,file)


def load_map():
    try:
        with open("map.json",encoding="utf-8") as file:
            info = json.load(file)
            return info
    except FileNotFoundError:
        return ""




