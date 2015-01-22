# -*- coding: utf-8 -*-
import sys

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

from util import *
import re

__author__ = 'chenliang'


def process_chu_ci():
    with open(get_relative_path(__file__, "raw/poems/楚辞")) as data_file:
        data_file_content = data_file.read().decode("UTF-8")
        # print data_file_content

        # poems = re.findall(ur'(^[^\s].*$\n)((^($|^\s+.*$)\n)+)', data_file_content, re.MULTILINE)
        poems = re.findall(ur'(^[^\s].*$\n)((^[^\w].*$\n)+)', data_file_content, re.MULTILINE)
        print len(poems)

        for poem in poems:
            print "--->".join(poem)
            # print poem


# process_chu_ci()

def get_files(path):
    result = []
    for root, dirs, files in os.walk(path):
        result.extend(map(lambda f: os.path.join(root, f), files))
    return result


def get_characters_in_poem_files(files):
    result = set()

    for poem_file_path in files:
        with open(poem_file_path) as poem_file:
            map(lambda k:result.add(k), filter(lambda ch: ch.strip() != "", poem_file.read().decode("utf-8")))

    return result

def generate_all_characters_in_poems():
    characters = get_all_characters_in_poem()
    with open(get_relative_path(__file__, "data/poem_characters"), "w") as poem_characters_file:
        poem_characters_file.write("{0}".format("".join(characters)))

def get_all_characters_in_poem():
    poem_files = get_files(get_relative_path(__file__, "raw/poems"))
    return get_characters_in_poem_files(poem_files)

# generate_all_characters_in_poems()

# print "importing opem"