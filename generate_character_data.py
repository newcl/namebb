# -*- coding: utf-8 -*-
__author__ = 'chenliang'

import os
import sys

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

from util import *


unicode_to_reading = {}
unicode_to_radical_count = {}
unicode_to_radical = {}

unicode_chinese_characters_in_reading = set()
unicode_chinese_characters_in_stroke = set()

def unicode_to_key(u):
    return "U+" + str(hex(ord(u)))[2:].upper()


def init_reading():
    with open(get_relative_path(__file__, "raw/read")) as read_file:
        lines = [line.strip() for line in read_file.read().decode().split("\n") if line.strip() != ""]
        for line in lines:
            segments = line.split("\t")
            unicode_to_reading[segments[0]] = segments[2]

            unicode_chinese_characters_in_reading.add(unichr(int("0x" + segments[0][2:], 16)))



def init_stroke_count():
    with open(get_relative_path(__file__, "raw/strokes")) as read_file:
        lines = read_file.read().decode().split("\n")
        for line in lines:
            segments = line.split("\t")
            key = unicode_to_key(segments[1])
            unicode_to_radical_count[key] = segments[2]
            unicode_to_radical[key] = segments[11].strip()
            unicode_chinese_characters_in_stroke.add(segments[1])



init_stroke_count()
init_reading()

# exit()
# generate all gbk characters
# using format
# separator is \t
# unicode pinyin radical stroke-count

def generate_gbk_character_data():
    count = 0
    with open(get_relative_path(__file__, "data/data"), "w") as data_file:
        for b1 in range(0xB0, 0xF8):
            for b2 in range(0xA1, 0xFF):
                if b2 == 0X7F:
                    continue

                if b1 == 0xd7 and (0xfa <= b2 <= 0xfe):
                    continue

                bs = bytearray()
                bs.append(b1)
                bs.append(b2)

                vs = bs.decode("GBK")

                key = unicode_to_key(vs)
                pinyin = unicode_to_reading[key]
                radical = unicode_to_radical[key]
                stroke_count = unicode_to_radical_count[key]
                count += 1
                data_file.write("{0}\t{1}\t{2}\t{3}\n".format(vs, pinyin, radical, stroke_count))

    print count


def generate_unicode_chinese_character_data():
    with open(get_relative_path(__file__, "data/character_data"), "w") as data_file:
        for unicode_chinese_character in unicode_chinese_characters_in_stroke:
            key = unicode_to_key(unicode_chinese_character)

            if key in unicode_to_reading:
                pinyin = unicode_to_reading[key]

                if key in unicode_to_radical:
                    radical = unicode_to_radical[key]
                    stroke_count = unicode_to_radical_count[key]

                    data_file.write("{0}\t{1}\t{2}\t{3}\n".format(unicode_chinese_character, pinyin, radical, stroke_count))
                else:
                    print unicode_chinese_character, " not found"


# check if our stroke and reading character library is bigger than the
# name library


# generate_unicode_chinese_character_data()

def verify():
    cs = set()

with open(get_relative_path(__file__, "raw/boy_names")) as name_file:
    names = filter(lambda name: name.strip() != "" ,name_file.read().decode("utf-8").split("\n"))
    map(lambda name: map(lambda c: cs.add(c), name), names)

    with open(get_relative_path(__file__, "raw/girl_names")) as name_file:
        names = filter(lambda name: name.strip() != "" ,name_file.read().decode("utf-8").split("\n"))
        map(lambda name: map(lambda c: cs.add(c), name), names)

    print "character in reading files ", len(unicode_chinese_characters_in_reading)
    print "character in stroke files ", len(unicode_chinese_characters_in_stroke)
    print "character in name files ", len(cs)

    # ps = unicode_chinese_characters_in_stroke - unicode_chinese_characters_in_stroke.intersection(unicode_chinese_characters_in_reading)
    # print len(ps)
    # for p in ps:
    #     print p

    assert cs.issubset(unicode_chinese_characters_in_stroke), ""