import json
import base64
import os
import timeit
import io
import pygame
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

def Call():
    data = {
               "Mana": 98,
               "Call_type": 22,
               "Ddistance": 56,
               "Cooldown": 54,
               "Rang": 3,
               "Icon": filedialog.askopenfile(),
               "Animation": loop1(filedialog.askdirectory())
           },

    with open("../Json/Magic.json", encoding='utf8') as f:
        data1 = json.load(f)
        data1['Magic'][0][''] = data
        with open("../Json/Magic.json", 'w', encoding='utf8') as f1:
            json.dump(data1, f1, ensure_ascii=False, indent=2)



def heal():
    data = {
               "Mana": 98798,
               "Heal": 98,
               "Ddistance": 56,
               "Cooldown": 54,
               "Rang": 3,
               "Icon": filedialog.askopenfile(),
               "Animation": loop1(filedialog.askdirectory())
           },

    with open("../Json/Magic.json", encoding='utf8') as f:
        data1 = json.load(f)
        data1[''] = data
        with open("../Json/Magic.json", 'w', encoding='utf8') as f1:
            json.dump(data1, f1, ensure_ascii=False, indent=2)
def Icon(src):
    print(src.name)
    with open(src.name, "rb", ) as image:
        return base64.b64encode(image.read()).decode('utf-8')



def loop1(src: str):
    images_list = []
    for img in os.listdir(src):
        image = open('{}/{}'.format(src, img), 'rb')
        images_list.append(base64.b64encode(image.read()).decode('utf-8'))
    return images_list


def Damage():
    data = {
               "Mana": 20,
               "Damage": 20,
               "Cooldown": 10,
               "Rang": 0,
               "Up_level_magic": 5,
               "Icon": Icon(filedialog.askopenfile()),
               "Animation": loop1(filedialog.askdirectory())
           },

    print(data)

    with open("../Json/Magic.json", encoding='utf8') as f:
        data1 = json.load(f)
        data1['Magiccirle'] = data
        with open("../Json/Magic.json", 'w', encoding='utf8') as f1:
            json.dump(data1, f1, ensure_ascii=False, indent=2)



Damage()


