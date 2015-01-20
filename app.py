# -*- coding: utf-8 -*-

__author__ = 'chenliang'



from flask import Flask, jsonify, request, render_template, current_app, logging
import random
import os

import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

from logging import handlers
from util import *

app = Flask(__name__)
app.debug = True

boy_name_files = []
girl_name_files = []

boy_name_file_prefix = "split_boy"
girl_name_file_prefix = "split_girl"

all_gbk_characters = {}

def init_logging():

    path = get_relative_path(__file__,"log/namebb.log")

    logger = handlers.RotatingFileHandler(path)
    # logger.setLevel(logging.DEBUG)
    app.logger.addHandler(logger)

def init_names():
    data_path = get_relative_path(__file__, "names")

    for root, dirs, files in os.walk(data_path):
        boy_name_files.extend([os.path.join(data_path, file) for file in files if file.startswith(boy_name_file_prefix)])
        girl_name_files.extend([os.path.join(data_path, file) for file in files if file.startswith(girl_name_file_prefix)])

@app.route('/')
def index():
    return render_template("index.html")


def random_name():
    if (random.randint(0,1) == 0) :
        current_app.logger.debug("generating boy name")
        return random_boy_name();
    else:
        current_app.logger.debug("generating girl name")
        return random_girl_name();

@app.route('/random')
def random_name():
    xing = request.args.get('xing')
    word_count = request.args.get('wordCount', 0)
    gender = request.args.get('gender', 'both')

    current_app.logger.debug("xing={0} gender={1} word_count={2}".format(xing, gender, word_count))

    name = ""
    if gender == "male":
        name = random_boy_name()
        current_app.logger.debug("random boy name={0} for xing{1}".format())
    elif gender == "female":
        name = random_girl_name()
    else:
        name = random_name()

    whole_name = xing + name

    reading = get_reading_for_name(whole_name)

    current_app.logger.debug("name={0} reading={1}".format(whole_name, "".join(reading)))

    return jsonify(n=[c for c in whole_name], r=reading)

# unicode pinyin radical stroke-count

# def get_name(gender="both", word_count=0):


def get_reading_for_character(c):
    return all_gbk_characters[c][1]

def get_reading_for_name(name):
    return [get_reading_for_character(c) for c in name]

def get_radical_for_xing(xing):
    assert len(xing) == 1
    return all_gbk_characters[xing][2]

def get_stroke_count_for_character(c):
    return all_gbk_characters[c][3]

@app.route('/rank')
def rank_name():
    return jsonify(score=random.randint(0, 100), name=request.args.get('name', ''))

def random_boy_name():
    return random_name(boy_name_files)

def random_girl_name():
    return random_name(girl_name_files)

def random_name(files):
    name_file_path = files[random.randint(0, len(files)-1)]
    with open(name_file_path) as name_file:
        names = [name for name in name_file.read().decode("utf-8").split("\n") if name.strip() != ""]
        return names[random.randint(0, len(names)-1)]

# 3、计天格法：如是复姓，姓的笔画相加，得出天格数；如是单姓，姓的笔画加一得出天格数。
# 4、计人格法：复姓复名姓氏的第二个字笔画加名的第一个字的笔画；复姓单名姓氏的第二个字加名的笔画；单姓复名是姓的笔画加名字的第一个字笔画；单姓单名是姓名相加的笔画数。
# 5、计地格法：复姓复名和单姓复名都是名字相加的数；复姓单名和单姓单名是名的笔画数加一。
# 6、计外格法：复姓复名是姓的第一个字和名的最后一个字相加的笔画数；复
# 姓单名是复姓第一个字的笔画数加一；单姓复名（是姓与名的最后一个字的笔画数之和？）应为最后一字笔画数加1；单姓单名统一为二。
# 7、计总格法：姓名笔画数的总和。
# 8、计算出了姓名的五格后，就是给五格配上阴、阳。数字超过十的只留个位数计算。如：15为还原成5，属阳土；52还原成2，属阴木，此类推。

# 1或6为水，2或7为火，3或8为木，4或9为金，5或10为土
# 1或2为木，3或4为火，5或6为土，7与8为金，9与0 <----------- 用这个
# 1、3、5、7、9属阳；2、4、6、8、10属阴
def get_wu_ge_attribute(ge):
    ge_value = ge % 10
    if ge_value == 0:
        ge_value = 10

    yin_yang = "?"
    if ge_value % 2 == 0:
        yin_yang = "阴"
    else:
        yin_yang = "阳"

    wu_xing = "?"
    if 1 <= ge_value <= 2:
        wu_xing = "木"
    elif 3 <= ge_value <= 4:
        wu_xing = "火"
    elif 5 <= ge_value <= 6:
        wu_xing = "土"
    elif 7 <= ge_value <= 8:
        wu_xing = "金"
    elif 9 <= ge_value <= 10:
        wu_xing = "水"

    return yin_yang + wu_xing



def get_wu_ge(xing, name):
    tian_ge = get_tian_ge(xing)
    ren_ge = get_ren_ge(xing, name)
    di_ge = get_di_ge(name)
    wai_ge = get_wai_ge(xing, name)
    zong_ge = get_zong_ge(xing, name)

    result = {}
    result["tian_ge"] = tian_ge
    result["tian_ge_att"] = get_wu_ge_attribute(tian_ge)

    result["ren_ge"] = ren_ge
    result["ren_ge_att"] = get_wu_ge_attribute(ren_ge)

    result["di_ge"] = di_ge
    result["di_ge_att"] = get_wu_ge_attribute(di_ge)

    result["wai_ge"] = wai_ge
    result["wai_ge_att"] = get_wu_ge_attribute(wai_ge)

    result["zong_ge"] = ren_ge
    result["zong_ge_att"] = get_wu_ge_attribute(zong_ge)

    return result


# 1或6为水，2或7为火，3或8为木，4或9为金，5或10为土


def get_wai_ge(xing, name):
    xing_count = len(xing)
    name_count = len(name)
    if xing_count == 2 and name_count == 2:
        return get_stroke_count_for_character(xing[0]) + get_stroke_count_for_character(name[1])
    elif xing_count == 2 and name_count == 1:
        return get_stroke_count_for_character(xing[0]) + 1
    elif xing_count == 1 and name_count == 2:
        return get_stroke_count_for_character(name[1]) + 1
    elif xing_count == 1 and name_count == 1:
        return 2

def get_zong_ge(xing, name):
    return sum([get_stroke_count_for_character(c) for c in xing+name])

def get_di_ge(name):
    count = len(name)
    if count == 1:
        return get_stroke_count_for_character(name[0]) + 1
    elif count == 2:
        return sum(get_stroke_count_for_character(c) for c in name)

def get_ren_ge(xing, name):
    count = len(xing)
    if count == 1:
        return get_stroke_count_for_character(xing[0]) + get_stroke_count_for_character(name[0])
    elif count == 2:
        return get_stroke_count_for_character(xing[1]) + get_stroke_count_for_character(name[0])

def get_tian_ge(xing):
    count = len(xing)
    if count == 1:
        return get_stroke_count_for_character(xing[0]) + 1
    elif count == 2:
        return sum([get_stroke_count_for_character(c) for c in xing])

def init_data():
    # unicode pinyin radical stroke-count
    with open(get_relative_path(__file__, "data/data")) as data_file:
        lines = [line for line in data_file.read().decode("utf-8").split("\n") if line.strip() != ""]
        for line in lines:
            fields = line.split("\t")
            all_gbk_characters[fields[0]] = fields

init_logging()
init_names()
init_data()


if __name__ == '__main__':
    app.run(host='0.0.0.0')

    
