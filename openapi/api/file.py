import flask
import os

static_dir = 'reports'

def render(filename):
    sdir = f'{static_dir}/'
    return flask.send_from_directory(sdir, filename)