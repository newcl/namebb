__author__ = 'chenliang'

import os

boy_name_one_character_file_prefix = "boy_1"
boy_name_two_character_file_prefix = "boy_2"

girl_name_one_character_file_prefix = "girl_1"
girl_name_two_character_file_prefix = "girl_2"

def load_name_data(path):
    # unicode pinyin radical stroke-count
    result = {}
    with open(path) as data_file:
        lines = [line for line in data_file.read().decode("utf-8").split("\n") if line.strip() != ""]
        for line in lines:
            fields = line.split("\t")
            result[fields[0]] = fields

    return result


def init_names(data_path):
    for root, dirs, files in os.walk(data_path):
        return (
            [os.path.join(data_path, file) for file in files if file.startswith(boy_name_one_character_file_prefix)],
            [os.path.join(data_path, file) for file in files if file.startswith(boy_name_two_character_file_prefix)],
            [os.path.join(data_path, file) for file in files if file.startswith(girl_name_one_character_file_prefix)],
            [os.path.join(data_path, file) for file in files if file.startswith(girl_name_two_character_file_prefix)])