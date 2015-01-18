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

def unicode_to_key(u):
    return "U+" + str(hex(ord(u)))[2:].upper()

def init_reading():
    data_path = get_relative_path(__file__, "data")
    with open(os.path.join(data_path, "read")) as read_file:
        lines = [line.strip() for line in read_file.read().decode().split("\n") if line.strip() != ""]
        for line in lines:
            segments = line.split("\t")
            unicode_to_reading[segments[0]] = segments[2]

def init_stroke_count():
    data_path = get_relative_path(__file__, "data")
    with open(os.path.join(data_path, "strokes")) as read_file:
        lines = read_file.read().decode().split("\n")
        for line in lines:

            segments = line.split("\t")
            key = unicode_to_key(segments[1])
            unicode_to_radical_count[key] = segments[2]
            unicode_to_radical[key] = segments[11].strip()


init_stroke_count()
init_reading()

# generate all gbk characters
# using format
# separator is \t
# unicode pinyin radical stroke-count
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

