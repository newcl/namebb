__author__ = 'chenliang'

#encoding = utf-8

from flask import Flask, jsonify, request, render_template
import random


app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template("index.html")

#
# type 1 for random character
# type 2 for random poem line
#
@app.route('/random')
def random_name():
    return jsonify(type=1, v=unichr(random.randint(0x4000, 0x4999)))


@app.route('/rank')
def rank_name():
    return jsonify(score=random.randint(0, 100), name=request.args.get('name', ''))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
