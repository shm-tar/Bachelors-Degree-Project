import os
import secrets
from flask import current_app, abort, Response


def update_file(upl_filename):
    random_hex = secrets.token_hex(8)
    f_ext = os.path.splitext(upl_filename.filename)[1]

    # extension and filesize check
    # flask automatically checks filesize using
    # current_app.config['MAX_CONTENT_LENGTH']) from config.py
    if f_ext not in current_app.config['UPLOAD_EXTENSIONS']:
        abort(Response('<b><h1>Wrong File Extension!</b>\n</h1>'
                       '<p>Please consider choosing '
                       'between <b>.doc, .docx or .pdf.</b></p>'))

    new_filename = random_hex + f_ext
    file_path = os.path.join(current_app.root_path, current_app.config['UPLOAD_PATH'], new_filename)
    upl_filename.save(file_path)
    return new_filename
