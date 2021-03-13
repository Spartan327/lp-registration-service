import json

def get_data(type_data):
    with open('data.json', 'r', encoding='utf-8') as f:
        all_data = json.loads(f.read())
    return all_data[type_data]
