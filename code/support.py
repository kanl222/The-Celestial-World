from csv import reader
from os import walk, listdir
import pygame
import base64
import io
import simplejson


def import_csv_layout(path):
    with open(path) as level_map:
        return [list(row) for row in reader(level_map, delimiter=',')]


def import_folder(path):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


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
        data = {}
        with open("../data/{}.json".format(name), 'r') as f1:
                file = f1.read()
                if not file: continue
                data = simplejson.loads(file)
                for i in data:
                    try:
                        keys = data[i].keys()
                        if 'sprite' in keys:
                            data[i]['sprite'] = import_folder_base64_image(data[i]['sprite'])
                        if 'data' in data[i].keys():
                            data[i]['data']['icon'] = import_folder_base64_image(data[i]['data']['icon'])
                        if 'icon' in data[i].keys():
                            data[i]['icon'] = import_folder_base64_image(data[i]['icon'])
                        if 'animation' in keys:
                            data[i]['animation'] = import_folder_base64_Animation(
                                data[i]['animation'])
                    except Exception as e:
                        print(e,i)
        files[name] = data
    return files
