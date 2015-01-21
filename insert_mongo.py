# -*- coding: utf-8 -*-

__author__ = 'chenliang'

from pymongo import *
from names import *

mongo = MongoClient('mongodb://localhost:27017/')

# print normalize_names()

mongo.app.names.insert(normalize_names())

# print mongo.app.names.find()
