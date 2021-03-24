import json


def get_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        all_data = json.loads(f.read())
    return all_data
