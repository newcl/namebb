# -*- coding: utf-8 -*-

__author__ = 'chenliang'

from flask import Flask, jsonify, request, render_template, current_app, logging
import random
import os

import sys

from name_data import *

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

from logging import handlers
from util import *
from wu_ge import *
from poem import *
from name_data import *


app = Flask(__name__)
app.debug = True


def init_logging():
    path = get_relative_path(__file__, "log/namebb.log")
    logger = handlers.RotatingFileHandler(path)
    # logger.setLevel(logging.DEBUG)
    app.logger.addHandler(logger)

@app.route('/')
def index():
    return render_template("index.html")


def get_name(xing, word_count, gender):
    print "params ", xing, word_count, gender
    if gender == "male":
        gender_for_data = "boy"
    elif gender == "female":
        gender_for_data = "girl"
    else:
        if random.randint(0, 1) == 0:
            gender_for_data = "boy"
        else:
            gender_for_data = "girl"

    if word_count == 1:
        word_count_for_data = 1
    elif word_count == 2:
        word_count_for_data = 2
    else:
        if random.randint(0, 1) == 0:
            word_count_for_data = 1
        else:
            word_count_for_data = 2

    target_files = []

    if gender_for_data == "boy" and word_count_for_data == 1:
        target_files = boy_name_one_character_files
    elif gender_for_data == "boy" and word_count_for_data == 2:
        target_files = boy_name_two_character_files

    if gender_for_data == "girl" and word_count_for_data == 1:
        target_files = girl_name_one_character_files
    elif gender_for_data == "girl" and word_count_for_data == 2:
        target_files = girl_name_two_character_files


    target_file_path = target_files[random.randint(0, len(target_files) - 1)]
    print "get name params", gender_for_data, word_count_for_data, target_file_path

    with open(target_file_path) as name_file:
        names = [name for name in name_file.read().decode("utf-8").split("\n") if name.strip() != ""]

        return names[random.randint(0, len(names) - 1)]


@app.route('/random')
def random_name():
    xing = request.args.get('xing')
    word_count = int(request.args.get('word_count'))
    gender = request.args.get('gender')

    print "xing={0} gender={1} word_count={2}".format(xing, gender, word_count)

    name = get_name(xing, word_count, gender)
    whole_name = xing + name

    reading = get_reading_for_name(whole_name)

    print "name={0} reading={1}".format(whole_name, "".join(reading))

    # scores
    # 1. referenced by poem
    # 2. total stroke counts
    # 3. wu_ge score
    #

    score = {}
    score["poem"] = get_poem_score(name)
    score["wuge"] = get_wu_ge_score(xing, name)
    score["stroke_count"] = get_stroke_count_score(name)

    for k in score:
        print k, "--->", score[k]
    response = jsonify(n=[c for c in whole_name], r=reading,score=score)

    return response

def get_stroke_count_score(name):
    return get_stroke_score(sum(map(lambda c:get_stroke_count_for_character(c), name)))


# def get_poem_score(name):
#     count = len(filter(lambda c:c in all_characters_in_poems, name))
#     return int(count*1.0*100/len(name))

@app.route('/rank')
def rank_name():
    return jsonify(score=random.randint(0, 100), name=request.args.get('name', ''))


# def random_name(files):
#     name_file_path = files[random.randint(0, len(files) - 1)]
#     with open(name_file_path) as name_file:
#         names = [name for name in name_file.read().decode("utf-8").split("\n") if name.strip() != ""]
#         return names[random.randint(0, len(names) - 1)]

init_logging()

boy_name_one_character_files, boy_name_two_character_files, girl_name_one_character_files, girl_name_two_character_files = init_names(get_relative_path(__file__, "names"))


if __name__ == '__main__':
    app.run(host='0.0.0.0')

    
