import json
import os
from pathlib import Path
from typing import Dict, List


SAVES_DIR = Path('saves')


def check_saves() -> bool:
    if SAVES_DIR.is_dir():
        return any(filter(lambda x: x.name.endswith('.json'), SAVES_DIR.glob('*')))
    return False


def load_saves() -> Dict:
    try:
        files = list(SAVES_DIR.glob('*.json'))
        files.sort(reverse=True)

        with open(files[0], encoding='utf-8', mode='r') as save:
            return json.load(save)
    except (FileNotFoundError, IndexError):
        print('No save files found.')
        return {}


def save(data: Dict) -> None:
    try:
        if not SAVES_DIR.is_dir():
            SAVES_DIR.mkdir()

        files = list(SAVES_DIR.glob('*.json'))
        if files:
            files.sort(reverse=True)
            file_num = int(files[0].stem) + 1
        else:
            file_num = 1

        file_name = f'{file_num}.json'
        save_path = SAVES_DIR / file_name

        with open(save_path, encoding='utf-8', mode='w') as file:
            json.dump(data, file)
    except Exception as e:
        print(f'Failed to save data. Error: {e}')
