import json
import os.path


__internal_json = json.load(open('accounts.json', 'r')) if os.path.exists('accounts.json') else {}


def create(username: str, password: str, toon: str):
    __internal_json[username] = {'password': password, 'toon': toon}
    json.dump(__internal_json, open('accounts.json', 'w'), indent=2)


def delete(username: str):
    del __internal_json[username]
    json.dump(__internal_json, open('accounts.json', 'w'), indent=2)


def exists(username: str):
    return username in __internal_json


def load() -> dict:
    return __internal_json
