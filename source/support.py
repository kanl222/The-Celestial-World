from csv import reader
from os import walk
import pygame
import base64
import io
import os
import json
from data import GameData

def import_csv_layout(path):
    with open(path) as level_map:
        return [list(row) for row in reader(level_map, delimiter=',')]



def import_folder(path, key_sorted=None):
    surface_list = []
    try:
        for _, __, img_files in os.walk(path):
            if key_sorted:
                sort_list = sorted(img_files,key=key_sorted)
            else:
                sort_list = sorted(img_files)
            for image in sort_list:
                full_path = os.path.join(path, image)
                image_surf = pygame.image.load(full_path).convert_alpha()
                surface_list.append(image_surf)

        return surface_list
    except FileNotFoundError as fnf_error:
        print("Не найдена указанная папка:", fnf_error)
    except pygame.error as pg_error:
        print("Ошибка Pygame при загрузке изображения:", pg_error)
    except Exception as e:
        print("Ошибка при импортировании папки:", e)



def import_image(path):
    try:
        image_surf = pygame.image.load(path).convert_alpha()
        return image_surf
    except FileNotFoundError as fnf_error:
        print("Не найдена указанная файл:", fnf_error)
        return None
    except pygame.error as pg_error:
        print("Ошибка Pygame при загрузке изображения:", pg_error)
        return None
    except Exception as e:
        print("Ошибка при импортировании файла:", e)
        return None


def import_animation(path, key_sorted=None):
    animation = {}
    elem_animetion = ['start','end','loops']
    try:
        for elem in elem_animetion:
            surface_list = []
            path_ = path + '/' + elem
            for _, __, img_files in os.walk(path_):
                if key_sorted:
                    sort_list = sorted(img_files,key=key_sorted)
                else:
                    sort_list = sorted(img_files)
                for image in sort_list:
                    full_path = os.path.join(path_, image)
                    image_surf = pygame.image.load(full_path).convert_alpha()
                    surface_list.append(image_surf)
            animation[elem] = surface_list
        print(animation)
        return animation
    except FileNotFoundError as fnf_error:
        print("Не найдена указанная папка:", fnf_error)
    except pygame.error as pg_error:
        print("Ошибка Pygame при загрузке изображения:", pg_error)
    except Exception as e:
        print("Ошибка при импортировании папки:", e)


def import_folder_base64_Animation(img_list:list):
    surface_list = []
    img_list.sort(key=lambda x: x[0])
    for image in img_list:
        image_surf = pygame.image.load(
            io.BytesIO(base64.b64decode(image[1].encode('utf-8')))).convert_alpha()

        if image_surf.get_size() <= (64, 64):
            image_surf = pygame.transform.scale(image_surf,
                                                (64,
                                                 64))
        if image_surf.get_size() >= (64, 64):
            image_surf = pygame.transform.scale(image_surf,
                                                (64,
                                                 64))
        surface_list.append(image_surf)
    return surface_list


def import_folder_base64_image(img):
    return pygame.image.load(
        io.BytesIO(base64.b64decode(img.encode('utf-8')))).convert_alpha()


def import_folder_json():
    filename = ['Object', 'Item', 'Magic', 'NPC', 'Enemy','Player']
    files = {}
    for name in filename:
        files[name] = GameData("../assets/{}.json".format(name))
    return files


def save_config(config:dict)->None:
    with open('../assets/config.json', encoding='utf-8', mode='w+') as file:
        save_ = json.dumps(config)
        file.write(save_)

def load_config()->dict:
    with open('../assets/config.json', encoding='utf-8', mode='r') as file:
        conf = json.loads(file.read())
        return conf


