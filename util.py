__author__ = 'chenliang'
import os

def get_relative_path(base, relative_path):
    path = os.path.dirname(os.path.realpath(base))
    return os.path.join(path, relative_path)

def get_items_in_file(file, separator="\n", encoding="utf-8"):
    with open(file) as data_file:
        return [line for line in data_file.read().decode(encoding).split(separator) if line.strip() != ""]

