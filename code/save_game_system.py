import os,json


def check_saves() -> bool:
    if os.path.exists('saves'):
        return any(filter(lambda x: '.json' in x, os.listdir('saves/')))
    return False

def load_saves() -> dict:
    saves = os.listdir('saves/')
    saves.sort(key=lambda x: int(x.split('.')[0]),reverse=True)
    with open(f'saves/{saves[0]}', encoding='utf-8', mode='r') as save:
        save_ = json.loads(save.read())
        return save_

def save(data:dict)->None:
    saves = os.listdir('saves/')
    if saves:
        saves = os.listdir('saves/')
        saves.sort(key=lambda x: int(x.split('.')[0]),reverse=True)
        file = f'{int(saves[0].split(".")[0])+1}.json'
    else:
        file = '1.json'
    with open(f'saves/{file}', encoding='utf-8', mode='w+') as file:
        save_ = json.dumps(data)
        file.write(save_)
