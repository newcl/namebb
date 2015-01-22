# -*- coding: utf-8 -*-
__author__ = 'chenliang'

from name_data import *
from util import *


# -*- coding: utf-8 -*-
__author__ = 'chenliang'

import re

def generate_wuge_data():
    with open(get_relative_path(__file__, "raw/wu_ge")) as wu_ge_file:
        wu_ge_detail = wu_ge_file.read().decode("utf-8")
        # all = re.findall('\d+数理', wu_ge_detail, re.MULTILINE)
        all = re.findall(ur'(\d+数理.*\n)((^.+$\n)+(^$))', wu_ge_detail, re.MULTILINE)
        # print len(all)

        with open(get_relative_path(__file__, "data/wu_ge"), "w") as wu_ge_data_file:
            for a in all:
                k = re.findall(ur'(\d+)数理、（([^）]*)）：([^（]*)（([^）]*)', a[0], re.UNICODE)
                wu_ge_data_file.write(("\t".join(k[0]) + "\n").encode("utf-8"))







# print len(re.findall('^\d+数理((?:\n.+)+)^$', wu_ge_detail, re.MULTILINE))
# print len(re.findall('^\d+数理.*^$\n', wu_ge_detail, re.MULTILINE))

# all = wu_ge_detail.split("^$\n")
# print len(all)

# all = re.findall('\d+数理.*',wu_ge_detail)
# for a in all:
#     print a
#     ms = re.findall('\d+数理[^（]（[^）]*）[^（]*（[^）]*）', a)
#     print len(ms)



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

def get_wu_ge_score(xing, name):
    wu_ge = get_wu_ge(xing, name)
    tian_ge_score = get_score(wu_ge["tian_ge"])
    di_ge_score = get_score(wu_ge["di_ge"])
    ren_ge_score = get_score(wu_ge["ren_ge"])
    wai_ge_score = get_score(wu_ge["wai_ge"])
    zong_ge_score = get_score(wu_ge["zong_ge"])

    return int((tian_ge_score+di_ge_score+ren_ge_score+wai_ge_score+zong_ge_score)*1.0/5)

def get_score(wu_ge):
    assert wu_ge in wu_ge_data, "not found " + wu_ge

    record = wu_ge_data[wu_ge]
    if record[3] == "吉":
        return 100
    elif record[3] == "半吉":
        return 60
    elif record[3] == "凶":
        return 10
    else:
        return 2


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
    return sum([get_stroke_count_for_character(c) for c in xing + name])


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

def load_wu_ge_data():
    with open(get_relative_path(__file__, "data/wu_ge")) as wu_ge_data_file:
        records = [record for record in wu_ge_data_file.read().decode("utf-8").split("\n") if record.strip() != ""]
        result = {}
        for record in records:
            fields = record.split("\t")
            result[int(fields[0])] = fields

        return result

# generate_wuge_data()
wu_ge_data = load_wu_ge_data()
# print wu_ge_data