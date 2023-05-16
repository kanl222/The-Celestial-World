import json

class GameData:
    def __init__(self, json_path):
        self.data = {}
        self.json_path = json_path
        self.load()

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
        self.save()

    def __delitem__(self, key):
        del self.data[key]
        self.save()

    def __len__(self):
        return len(self.data)

    def __index__(self, key):
        return self.data.index(key)

    def __contains__(self, key):
        return key in self.data

    def load(self):
        try:
            with open(self.json_path) as f:
                self.data = json.load(f)
        except json.JSONDecodeError:
            self.data = {}

    def save(self):
        with open(self.json_path, 'w') as f:
            json.dump(self.data, f)

    def update(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key, None)

    def clear(self):
        self.data = {}
        self.save()
