import json

data = {}


def load_data():
    with open('lab1/data.json') as f:
        data = json.load(f)
    return data


def parse_json(data, level=0):
    for key, value in data.items():
        print(f'{" " * level}Key: {key}')
        if isinstance(value, dict) and value:
            parse_json(value, level + 2)
        else:
            print(f'{" " * (level + 2)}Value is empty or not a dictionary')


data = load_data()
parse_json(data)
