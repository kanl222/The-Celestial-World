from csv import reader
from os import walk, listdir
import pygame
import base64
import io
import simplejson


def import_csv_layout(path):
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        return [list(row) for row in layout]


def import_folder(path):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def import_folder_base64_Animation(img_list):
    surface_list = []
    for image in img_list:
        image_surf = pygame.image.load(
            io.BytesIO(base64.b64decode(image.encode('utf-8')))).convert_alpha()
        if image_surf.get_size() <= (64, 64):
            image_surf = pygame.transform.scale(image_surf,
                                                (image_surf.get_size()[0] * 3,
                                                 image_surf.get_size()[1] * 3))
        surface_list.append(image_surf)
    return surface_list


def import_folder_base64_Icon(img):
    return pygame.image.load(
        io.BytesIO(base64.b64decode(img.encode('utf-8')))).convert_alpha()


def import_folder_json():
    filename = ['Object', 'Item', 'Magic', 'NPC', 'Enemy']
    files = {}
    for name in filename:
        res = []
        with open("../Json/{}.json".format(name), 'r') as f1:
                file = f1.read()
                if not file:
                    res.append([])
                    continue
                data = simplejson.loads(file)
                for i in data:
                    if data[i]['Animation'] is None and not data[i]['Icon'] is None:
                        pass
                    elif not data[i]['Animation'] is None and not data[i]['Icon'] is None:
                        data[i]['Animation'] = import_folder_base64_Animation(
                            data[i]['Animation'])
                res.append(data)
        files[name] = res
    return files
