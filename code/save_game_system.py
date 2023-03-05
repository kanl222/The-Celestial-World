import os
import json
from typing import Dict, List

SAVES_PATH = 'saves'

def check_saves() -> bool:
    """
    Check if any saves exist.

    Returns:
        bool: True if there are save files, False otherwise.
    """
    if os.path.exists(SAVES_PATH):
        return any(filter(lambda x: '.json' in x, os.listdir(f'{SAVES_PATH}/')))
    return False

def load_saves() -> Dict:
    """
    Load the latest save file.

    Returns:
        dict: The data from the latest save file.
    """
    files = [f for f in os.listdir(SAVES_PATH) if f.endswith('.json')]
    files.sort(reverse=True)
    with open(os.path.join(SAVES_PATH, files[0]), encoding='utf-8', mode='r') as save:
        return json.load(save)

def save(data: Dict) -> None:
    """
    Save the data to a file.

    Args:
        data (dict): The data to save.
    """
    if not os.path.exists(SAVES_PATH):
        os.makedirs(SAVES_PATH)
    files = [f for f in os.listdir(SAVES_PATH) if f.endswith('.json')]
    if files:
        files.sort(reverse=True)
        file_num = int(files[0].split('.')[0]) + 1
    else:
        file_num = 1
    file_name = f'{file_num}.json'
    with open(os.path.join(SAVES_PATH, file_name), encoding='utf-8', mode='w+') as file:
        json.dump(data, file)
