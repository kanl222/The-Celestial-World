import base64
import csv
import io
import json
import os
from pathlib import Path
import pygame
from data import GameData

# Корень проекта — папка The-Celestial-World (родитель source/)
# Определяется относительно файла, а не CWD — работает из любой директории запуска
BASE_DIR: Path = Path(__file__).resolve().parent.parent

def resolve_path(path) -> Path:
    """Resolves any relative path to an absolute path based on BASE_DIR.
    Handles relative paths starting with '../' (relative to source/)
    as well as paths relative to the project root directory.
    """
    p_str = str(path).replace('\\', '/')
    if p_str.startswith('../'):
        return BASE_DIR / p_str[3:]
    p = Path(path)
    if p.is_absolute():
        return p
    return BASE_DIR / p

def import_csv_layout(path):
    resolved = resolve_path(path)
    with open(resolved) as level_map:
        return [list(row) for row in csv.reader(level_map, delimiter=',')]

def import_folder(path, key_sorted=None):
    surface_list = []
    resolved = resolve_path(path)
    try:
        for _, __, img_files in os.walk(resolved):
            if key_sorted:
                sort_list = sorted(img_files, key=key_sorted)
            else:
                sort_list = sorted(img_files)
            for image in sort_list:
                full_path = os.path.join(resolved, image)
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
    resolved = resolve_path(path)
    try:
        image_surf = pygame.image.load(resolved).convert_alpha()
        return image_surf
    except FileNotFoundError as fnf_error:
        print("Не найден указанный файл:", fnf_error)
        return None
    except pygame.error as pg_error:
        print("Ошибка Pygame при загрузке изображения:", pg_error)
        return None
    except Exception as e:
        print("Ошибка при импортировании файла:", e)
        return None

def import_animation(path, key_sorted=None):
    """Загружает анимацию из папок start/end/loops в указанном пути."""
    animation = {}
    elem_animation = ['start', 'end', 'loops']
    resolved = resolve_path(path)
    try:
        for elem in elem_animation:
            surface_list = []
            path_ = os.path.join(resolved, elem)
            for _, __, img_files in os.walk(path_):
                if key_sorted:
                    sort_list = sorted(img_files, key=key_sorted)
                else:
                    sort_list = sorted(img_files)
                for image in sort_list:
                    full_path = os.path.join(path_, image)
                    image_surf = pygame.image.load(full_path).convert_alpha()
                    surface_list.append(image_surf)
            animation[elem] = surface_list
        return animation
    except FileNotFoundError as fnf_error:
        print("Не найдена указанная папка:", fnf_error)
    except pygame.error as pg_error:
        print("Ошибка Pygame при загрузке изображения:", pg_error)
    except Exception as e:
        print("Ошибка при импортировании папки:", e)

def import_folder_base64_Animation(img_list: list) -> list:
    """Загружает анимацию из base64-кодированных строк и нормирует размер до 64x64."""
    surface_list = []
    img_list.sort(key=lambda x: x[0])
    for image in img_list:
        image_surf = pygame.image.load(
            io.BytesIO(base64.b64decode(image[1].encode('utf-8')))).convert_alpha()
        if image_surf.get_size() != (64, 64):
            image_surf = pygame.transform.scale(image_surf, (64, 64))
        surface_list.append(image_surf)
    return surface_list

def import_folder_base64_image(img):
    return pygame.image.load(
        io.BytesIO(base64.b64decode(img.encode('utf-8')))).convert_alpha()

def import_folder_json() -> dict:
    """Загружает все JSON-файлы игровых данных из assets/."""
    filename = ['Object', 'Item', 'Magic', 'NPC', 'Enemy', 'Player']
    files = {}
    for name in filename:
        files[name] = GameData(str(BASE_DIR / 'assets' / f'{name}.json'))
    return files

def save_config(config: dict) -> None:
    """Сохраняет конфигурацию в assets/config.json."""
    config_path = BASE_DIR / 'assets' / 'config.json'
    config_path.write_text(json.dumps(config), encoding='utf-8')

def load_config() -> dict:
    """Загружает конфигурацию из assets/config.json."""
    config_path = BASE_DIR / 'assets' / 'config.json'
    return json.loads(config_path.read_text(encoding='utf-8'))
