__author__ = 'chenliang'

#encoding = utf-8

from flask import Flask, jsonify, request, render_template, current_app, logging
import random
import os

from logging import handlers



app = Flask(__name__)
app.debug = True

boy_name_files = []
girl_name_files = []

boy_name_file_prefix = "split_boy"
girl_name_file_prefix = "split_girl"

def init_logging():

    path = os.path.dirname(os.path.realpath(__file__))

    logger = handlers.RotatingFileHandler(os.path.join(path,"log/namebb.log"))
    # logger.setLevel(logging.DEBUG)
    app.logger.addHandler(logger)


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

    current_app.logger.debug("xing={0} gender={1} word_count={2}".format(xing, gender, word_count))

    name = ""
    if (random.randint(0,1) == 0) :
        current_app.logger.debug("generating boy name")
        name = random_boy_name();
    else:
        current_app.logger.debug("generating girl name")
        name = random_girl_name();

    current_app.logger.debug("about to return".format("{0}", name))
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

init_logging()
init_name_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
