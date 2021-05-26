import os
from flask import json
from pathlib import Path


def __get_json_file_path():
    root_path = os.path.realpath(os.path.dirname(__file__))
    file_name = 'inventory' + '.json'
    file_path = Path(os.path.join(
        root_path, "./" + file_name))

    return file_path


def __load_json_file():
    data = None
    file_path = None

    file_path = __get_json_file_path()

    with open(file_path, encoding="utf8") as json_file:
        data = json.load(json_file)
    return data


def __is_json_file_existed():
    file_path = __get_json_file_path()

    return file_path.is_file()


def get_all_inventory():
    data = __load_json_file()
    new_data = []

    for item in data:
        new_data.append({
            'id': item['id'],
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'total_amount': item['total_amount'],
        })

    response_object = {
        'status': 'SUCCESS',
        'message': 'Successfully getting data of inventory!',
        'data': {
            'inventory': new_data
        }
    }

    return response_object, 200


def get_by_id_inventory(id):
    data = __load_json_file()
    list_item = list(filter(lambda item: item['id'] == int(id), data))[0]
    list_item['histories'].reverse()

    response_object = {
        'status': 'SUCCESS',
        'message':  'Successfully getting data of inventory!',
        'data': list_item
    }
    return response_object, 200
