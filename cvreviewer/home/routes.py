import os
from flask import (Blueprint, render_template, send_from_directory,
                    current_app, flash)
from flask_login import login_required

home = Blueprint('home', __name__)


@home.route('/')
@home.route('/index')
def index():
    return render_template('index.html')


@home.route('/upload_cv')
@login_required
def upload_cv_render():
    flash('Upload your .pdf or .docx CV')
    return render_template('upload_cv.html', title='Upload a CV')


@home.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                               'favicon.png', mimetype='image/vnd.microsoft.icon')
