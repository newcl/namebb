
# -*- coding: utf-8 -*-
__author__ = 'chenliang'

from name_data import *
from util import *

all_characters = load_name_data(get_relative_path(__file__, "data/data"))
print len(all_characters)

# exit()
boy_name_one_character_files, boy_name_two_character_files, girl_name_one_character_files, girl_name_two_character_files = init_names(get_relative_path(__file__, "names"))

files = boy_name_one_character_files + boy_name_two_character_files + girl_name_one_character_files + girl_name_two_character_files

for file in files:
    with open(file) as name_file:
        names = [name for name in name_file.read().decode("utf-8").split("\n") if name.strip() != ""]
        invalid_names = filter(lambda name: len(filter(lambda c: c not in all_characters, name)) > 0, names)
        if len(invalid_names) > 0:
            print "invalid in ", file
            for n in invalid_names:
                print n

