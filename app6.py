import os
import pandas as pd
from flask import Flask, request, render_template, redirect, url_for, request, send_from_directory, flash, session
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from werkzeug.utils import secure_filename
import datetime
import shutil


# from os.path import join, dirname, realpath

project_root = os.path.dirname(__file__)
print(project_root)
template_path = os.path.join(project_root, 'app/templates')


server = flask.Flask(__name__)

# Setup Upload Folder
cwd = os.getcwd()
UPLOAD_FOLDER = os.path.join(cwd, 'uploads')
print(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = {'csv'}

#Configure Server / Flask Object
server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
server.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
server.config['UPLOAD_EXTENSIONS'] = ['.csv']
server.config['SECRET_KEY'] = '6WX9PIg8zdrQHqwwDVOS_Q'


@server.route('/')
def render_index():
    """index.html"""
    return render_template('index.html', author = 'Calvin')


if __name__ == '__main__':
    server.run(debug=True)

