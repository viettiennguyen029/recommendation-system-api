import os
from flask import json
from pathlib import Path


class LanguageHelper:
    def __init__(self, args):
        self.data = self.__load_language_file(args)

    def __get_language_code(self, args):
        language_code = 'vi'

        if 'language' in args:
            language_code = args['language']

        return language_code

    def __get_language_file_path(self, language_code):
        root_path = os.path.realpath(os.path.dirname(__file__))
        file_name = language_code + '.json'
        file_path = Path(os.path.join(
            root_path, "../languages/" + file_name))

        return file_path

    def __is_language_file_existed(self, language_code):
        file_path = self.__get_language_file_path(language_code)

        return file_path.is_file()

    def __load_language_file(self, args):
        data = None
        file_path = None
        language_code = self.__get_language_code(args)

        if self.__is_language_file_existed(language_code):
            file_path = self.__get_language_file_path(language_code)
        else:
            file_path = self.__get_language_file_path('vi')

        with open(file_path, encoding="utf8") as language_file:
            data = json.load(language_file)

        return data

    def get_message(self, query_string):
        data = self.data
        keys = query_string.split('.')

        for key in keys:
            data = data[key]

        return data
