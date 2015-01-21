__author__ = 'chenliang'

from util import *

boy_name_file_prefix = "split_boy"
girl_name_file_prefix = "split_girl"

def normalize_names():
    data_path = get_relative_path(__file__, "names")
    normalized_names = []
    for root, dirs, files in os.walk(data_path):
        boy_name_files = [os.path.join(data_path, file) for file in files if file.startswith(boy_name_file_prefix)]
        for boy_name_file in boy_name_files:
            normalized_names.extend(normalize(load_names(boy_name_file), "male"))

        girl_name_files = [os.path.join(data_path, file) for file in files if file.startswith(girl_name_file_prefix)]
        for girl_name_file in girl_name_files:
            normalized_names.extend(normalize(load_names(girl_name_file), "female"))

    return normalized_names


def load_names(path):
    with open(path) as name_file:
        return [name for name in name_file.read().decode("utf-8").split("\n") if name.strip() != ""]

def normalize(names, gender):
    result = []
    for name in names:
        record = {}
        record["name"] = name
        record["gender"] = gender
        record["word_count"] = len(name)

        result.append(record)
    return result