import os
import pandas as pd
from flask import Flask, request, render_template, redirect, url_for, request, send_from_directory, flash, session
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from werkzeug.utils import secure_filename
# from os.path import join, dirname, realpath

project_root = os.path.dirname(__file__)
print(project_root)
template_path = os.path.join(project_root, 'app/templates')


server = flask.Flask(__name__)

# Setup Upload Folder
cwd = os.getcwd()
UPLOAD_FOLDER = os.path.join(cwd, 'uploads')
ALLOWED_EXTENSIONS = {'csv'}

#Configure Server / Flask Object
server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
server.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
server.config['UPLOAD_EXTENSIONS'] = ['.csv']



@server.route('/')
def render_index():
    """index.html"""
    return render_template('index.html', author = 'Calvin')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@server.route('/upload_site', methods=['GET', 'POST'])
def upload_file1():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(server.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>'''


##************************************
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, server=server, url_base_pathname='/dashapp/', external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])
#===========================================================

app = dash.Dash(__name__, server=server, url_base_pathname='/dashapp_tims/', external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

url = 'http://calvinbrown32.github.io/Collisions.csv'
crash_data = pd.read_csv(url)
#  crash_data.set_index(['CASE_ID'], inplace=True)
#  crash_data.index.name = None
bike_crashes = crash_data.loc[crash_data.BICYCLE_ACCIDENT == 'Y']
ped_crashes = crash_data.loc[crash_data.PEDESTRIAN_ACCIDENT == 'Y']

#Create table of total crashes by year
df_bike = bike_crashes['ACCIDENT_YEAR'].value_counts().reset_index()
df_bike.columns = ['ACCIDENT_YEAR', 'total']


fig = px.bar(df_bike, x="ACCIDENT_YEAR", y="total", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

#============================================




@server.route('/test_page/<test_pg_num>')
def test_page(test_pg_num):
    """This flask route  demonstrates variable rules """
    return 'This is test page ' + str(test_pg_num)

@server.route('/data_test')
def data_test():
    """Tests a number of functions including downloading a csv file from my github, and
    loading it to an html page"""

    # Download and munge the crash data from Github account
    url = 'http://calvinbrown32.github.io/Collisions.csv'
    crash_data = pd.read_csv(url)
    bike_crashes = crash_data.loc[crash_data.BICYCLE_ACCIDENT == 'Y']
    ped_crashes = crash_data.loc[crash_data.PEDESTRIAN_ACCIDENT == 'Y']

    return render_template('data_test.html', tables=[bike_crashes.to_html(classes='bike'), ped_crashes.to_html(classes='ped')],
                           titles=['na', 'Bike Crashes', 'Ped Crashes'])



#===============================================
# UPLOAD SITE V2
# FROM: https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
#===============================================



@server.route(f'/{UPLOAD_FOLDER}/<filename>')
def uploaded_file(filename):
    return send_from_directory(server.config['UPLOAD_FOLDER'],
                               filename)

#===============================================
# Trying to Print out uploaded file list
# https://stackoverflow.com/questions/49385103/return-list-of-previously-uploaded-files-back-to-flask
# https://stackoverflow.com/questions/19911106/flask-file-upload-limit
# URL FOR EXPLANATION
#https://stackoverflow.com/questions/7478366/create-dynamic-urls-in-flask-with-url-for
#===============================================



# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload


#==============================
# The following code is used to test upload and deletion of files in dropzone window
#==============================

@server.route('/upload_site3')
def upload_file3():
    files = os.listdir(server.config['UPLOAD_FOLDER'])
    return render_template('/file_upload3.html', files=files)

@server.route('/upload_site3', methods=['GET', 'POST'])
def upload_files3():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in server.config['UPLOAD_EXTENSIONS']:
            return "This type of file is not permitted", 400
        uploaded_file.save(os.path.join(server.config['UPLOAD_FOLDER'], filename))
    return '', 204

@server.route('/upload_site4')
def upload_file4():
    files = os.listdir(server.config['UPLOAD_FOLDER'])
    return render_template('/file_upload4.html', files=files)

@server.route('/upload_site4', methods=['GET', 'POST'])
def upload_files4():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in server.config['UPLOAD_EXTENSIONS']:
            return "This type of file is not permitted", 400
        uploaded_file.save(os.path.join(server.config['UPLOAD_FOLDER'], filename))
    return '', 204


# Source:
# https://stackoverflow.com/questions/51913220/simple-flask-app-server-passing-data-with-ajax-and-jquery

@server.route('/process_files', methods=['GET', 'POST'])
def process_files():
    filename = secure_filename(request.form['filename'])
    print(filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    os.remove(file_path)
    return 'success', 204

@server.route('/deletefile')
def delete_file():
    filename = secure_filename(request.form['filename'])
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    os.remove(file_path)


@server.route('/portfolio')
def render_portfolio():
    """portfolio_website.html"""
    return render_template('portfolio_website.html', author = 'Calvin')


@server.route('/portfolio2')
def render_portfolio2():
    """portfolio_website.html"""
    return render_template('portfolio_website2.html', author = 'Calvin')


@server.route('/portfolio_template')
def render_new_portfolio_template():
    """new_portfolio_template.html"""
    return render_template('new_portfolio_template.html', author = 'Calvin')

@server.route('/arrow_highway')
def render_arrow_hwy():
    """new_portfolio_template.html"""
    return render_template('portfolio_arrow_hwy.html', author = 'Calvin')

@server.route('/essays')
def render_essays():
    """essays.html"""
    return render_template('essays.html', author = 'Calvin')

@server.route('/death_and_life_revisited')
def render_death_and_life_revisited():
    """death_and_life_revisited.html"""
    return render_template('death_and_life_revisited.html', author = 'Calvin')

@server.route('/resume')
def render_resume():
    """resume.html"""
    return render_template('resume.html', author = 'Calvin')

@server.route('/jupyter_mode_share')
def render_jupyter_mode_share():
    """jupyter_mode_share.html"""
    return render_template('jupyter_mode_share.html', author = 'Calvin')

@server.route('/TriMet')
def render_TriMet():
    """trimet.html"""
    return render_template('trimet.html', author = 'Calvin')

@server.route('/commute_into_manhattan')
def render_commute_into_manhattan():
    """commute_into_manhattan.html"""
    return render_template('commute_into_manhattan.html', author = 'Calvin')

@server.route('/last_stop')
def render_last_stop():
    """last_stopn.html"""
    return render_template('last_stop.html', author = 'Calvin')

@server.route('/dcp_area_map')
def render_dcp_area_map():
    """last_stopn.html"""
    return render_template('dcp_area_map.html', author = 'Calvin')

@server.route('/hunter_college_projects')
def render_hunter_college_projects():
    """hunter_college_projects.html"""
    return render_template('hunter_college_projects.html', author = 'Calvin')

@server.route('/golden_gate_study')
def render_golden_gate_study():
    """golden_gate_study.html"""
    return render_template('golden_gate_study.html', author = 'Calvin')

@server.route('/contact')
def render_contact():
    """contact.html"""
    return render_template('contact.html', author = 'Calvin')

if __name__ == '__main__':
    server.run(debug=True)

