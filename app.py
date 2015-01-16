__author__ = 'chenliang'

#encoding = utf-8

from flask import Flask, jsonify, request, render_template
import random
import os


app = Flask(__name__)
app.debug = True

boy_name_files = []
girl_name_files = []

boy_name_file_prefix = "split_boy"
girl_name_file_prefix = "split_girl"

def init_name_db():
    for root, dirs, files in os.walk("./data"):
        boy_name_files.extend(["./data/" + file for file in files if file.startswith(boy_name_file_prefix)])
        girl_name_files.extend(["./data/" + file for file in files if file.startswith(girl_name_file_prefix)])

@app.route('/')
def index():
    return render_template("index.html")

#
# type 1 for random character
# type 2 for random poem line
#
@app.route('/random')
def random_name():
    xing = request.args.get('xing', '')
    print "xnig --->", xing
    word_count = request.args.get('wordCount', 0)
    gender = request.args.get('gender', 'both')

    name = ""
    if (random.randint(0,1) == 0) :
        name = random_boy_name();
    else:
        name = random_girl_name();
    return jsonify(n=name)


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

init_name_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
