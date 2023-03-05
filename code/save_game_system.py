import os, json


def check_saves() -> bool:
    if os.path.exists('saves'):
        return any(filter(lambda x: '.json' in x, os.listdir('saves/')))
    return False


def load_saves() -> dict:
    try:
        saves = os.listdir('saves/')
    except FileNotFoundError:
        return {}
    saves.sort(key=lambda x: int(x.split('.')[0]), reverse=True)
    with open(f'saves/{saves[0]}', encoding='utf-8', mode='r') as save:
        save_ = json.loads(save.read())
        return save_


def write_file(data: dict) -> None:
    savespath = 'saves'
    file = '1.json'
    if not os.path.exists(savespath):
        os.makedirs(savespath)
    if os.path.exists(savespath):
        saves = os.listdir(f'{savespath}/')
        saves.sort(key=lambda x: int(x.split('.')[0]), reverse=True)
        file = f'{int(saves[0].split(".")[0]) if saves else 1 + 1}.json'

    with open(f'{savespath}/{file}', encoding='utf-8', mode='w+') as file:
        file.write(json.dumps(data))
