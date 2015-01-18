__author__ = 'chenliang'
import os

def get_relative_path(base, relative_path):
    path = os.path.dirname(os.path.realpath(base))
    return os.path.join(path, relative_path)

