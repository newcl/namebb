__author__ = 'chenliang'

import os

def generate_all_characters_from_all_boys_and_girls_names():
    base_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(base_path,"data/character")

    all_characters = set()
    with open(path, "w") as character_file:
        data_path = os.path.join(base_path, "names")
        for root, dirs, files in os.walk(data_path):
            name_file_paths = [os.path.join(data_path, file) for file in files if file.startswith("split_")]
            for name_file_path in name_file_paths:
                with open(name_file_path) as name_file:
                    content = [c for c in name_file.read().decode("utf-8") if c.strip() != ""]
                    for c in content:
                        if c.isdigit():
                            print c
                            continue
                        all_characters.add(c)

        print len(all_characters)
        for c in all_characters:
            character_file.write("{0}\n".format(c.encode("utf-8")))




generate_all_characters_from_all_boys_and_girls_names()