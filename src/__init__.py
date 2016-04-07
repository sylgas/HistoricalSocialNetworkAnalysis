import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
RESOURCES_DIR = os.path.join(BASE_DIR, 'resources')


def get_resource(name):
    path = os.path.join(RESOURCES_DIR, name)
    file = open(path, 'r')
    return file.read()
