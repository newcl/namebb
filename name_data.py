__author__ = 'chenliang'

import os

from util import *

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

def get_reading_for_character(c):
    return all_gbk_characters[c][1]


def get_reading_for_name(name):
    return [get_reading_for_character(c) for c in name]


def get_radical_for_xing(xing):
    assert len(xing) == 1
    return all_gbk_characters[xing][2]


def get_stroke_count_for_character(c):
    return int(all_gbk_characters[c][3])

def get_name_stroke_count(file_path):
    with open(file_path) as name_data_file:
        result = set()
        names = [name for name in name_data_file.read().decode("utf-8").split("\n") if name.strip() != ""]
        for name in names:
            result.add(sum(map(lambda c:get_stroke_count_for_character(c), name)))

        return result

def generate_names_stroke_data():
    with open(get_relative_path(__file__, "data/stroke_data"), "w") as data_file:
        stroke_counts = get_name_stroke_count(get_relative_path(__file__, "raw/boy_names"))
        stroke_counts = stroke_counts.union(get_name_stroke_count(get_relative_path(__file__, "raw/girl_names")))

        data_file.write("\n".join([str(c) for c in stroke_counts]).encode("utf-8"))

def load_name_stroke_data():
    stroke_counts = map(lambda count:int(count), get_items_in_file(get_relative_path(__file__, "data/stroke_data")))
    stroke_counts.sort()
    # print stroke_counts
    return stroke_counts

def get_stroke_score(stroke):
    normalized = 1 - ((all_names_stroke_count.index(stroke)+1)*1.0/len(all_names_stroke_count))
    return int(10 + normalized*80)

all_gbk_characters = load_name_data(get_relative_path(__file__, "data/character_data"))
all_names_stroke_count = load_name_stroke_data()


# generate_names_stroke_data()