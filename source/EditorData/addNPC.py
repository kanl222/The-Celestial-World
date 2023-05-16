import json
import base64
import os
import re
from tkinter import filedialog


def Animation(src: str):
    images_list = []
    files = os.listdir(src)
    files.sort(key=lambda f: int(re.sub('\D', '', f)))
    print(files)
    for count, img in enumerate(files):
        image = open('{}/{}'.format(src, img), 'rb')
        images_list.append([count, base64.b64encode(image.read()).decode('utf-8')])
    return images_list


def Image(src):
    with open(src.name, "rb", ) as image:
        return base64.b64encode(image.read()).decode('utf-8')


def Add(data, path):
    with open(path, encoding='utf8') as f:
        try:
            data1 = json.load(f)
            last_id = max(map(int, data1.keys()))
            data1[last_id + 1] = data
            with open(path, 'w', encoding='utf8') as f1:
                json.dump(data1, f1, ensure_ascii=False, indent=2)
        except Exception:
            data1 = {}
            data1[1] = data
            with open(path, 'w', encoding='utf8') as f1:
                json.dump(data1, f1, ensure_ascii=False, indent=2)


def AddNpc():
    path = "../../data/NPC.json"
    Npc = {
        "Name": "Cube",
        "Image": Image(filedialog.askopenfile()),
    }
    open(f'../../data/dialogs/{Npc["Name"]}.json', "w+")
    Add(Npc, path)


AddNpc()
