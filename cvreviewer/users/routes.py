import re
from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from cvreviewer.models import User, ProcessedFile, Connections
from cvreviewer import db, bcrypt
from cvreviewer.users.utils import update_file

users = Blueprint('users', __name__)
auth = HTTPBasicAuth()

adm_user = {
    "tarasAdm": generate_password_hash("KiriNo54")
}


@auth.verify_password
def verify_password(uname, passw):
    if uname in adm_user and \
            check_password_hash(adm_user.get(uname), passw):
        return True
    else:
        return False


@users.route('/login')
def login():
    if current_user.is_authenticated:
        flash('You are already logged in!', 'info')
        return redirect(url_for('home.index'))
    if request.args.get('input_email'):
        input_email = request.args.get('input_email')
    else:
        input_email = ""
    return render_template('log_in.html', title='Log in',
                           input_email=input_email)


@users.route('/login', methods=['POST'])
def member_login():
    user = User.query.filter_by(email=request.form['email']).first()
    if user and bcrypt.check_password_hash(user.password, request.form['passw']):
        login_user(user)
        # check if user actually came from somewhere, so he gets there after login
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('home.index'))
    else:
        flash('Wrong email/password!')
        input_email = request.form['email']
        return redirect(url_for('users.login', input_email=input_email))


@users.route('/signup')
def signup():
    if current_user.is_authenticated:
        flash('You are already signed up!', 'info')
        return redirect(url_for('home.index'))
    return render_template('sign_up.html', title='Sign up')


@users.route('/signup', methods=['POST'])
def member_signup():
    # checking if user with the same email already exists
    if User.query.filter_by(email=request.form['email']).first() is not None:
        flash('Your user already exists!', 'error')
        return redirect(url_for('users.signup'))

    hashed_passw = bcrypt.generate_password_hash(request.form['passw']).decode('utf-8')
    user = User(email=request.form['email'], password=hashed_passw)
    db.session.add(user)
    db.session.commit()
    flash('Success!', 'success')
    return redirect(url_for('users.login'))


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.index'))


@users.route('/account')
@login_required
def account():
    pdf_file = url_for('static', filename='uploads/' + current_user.user_uploaded_file)
    post = ProcessedFile.query.get(current_user.id)

    sent_connections = Connections.query.filter_by(user_id_sends=current_user.id).all()

    sent_connections_num = 0
    connected_users = []
    incoming_reqs = []
    for i in range(len(sent_connections)):
        if sent_connections[i].are_connected is False:
            sent_connections_num += 1

        if (current_user.id == sent_connections[i].user_id_sends and
                sent_connections[i].are_connected is True):
            user = User.query.filter_by(id=sent_connections[i].user_id_recieves).first()
            connected_users.append((user.id, user.email))

        if (current_user.id == sent_connections[i].user_id_recieves and
                sent_connections[i].are_connected is False):
            user = User.query.filter_by(id=sent_connections[i].user_id_sends).first()
            incoming_reqs.append((user.id, user.email))

    # if your contact received a request and accepted it - he should appear in your list
    sent_connections_tmp = Connections.query.filter_by(user_id_recieves=current_user.id).all()
    for i in range(len(sent_connections_tmp)):
        if (current_user.id == sent_connections_tmp[i].user_id_recieves and
                sent_connections_tmp[i].are_connected is True):
            user = User.query.filter_by(id=sent_connections_tmp[i].user_id_sends).first()
            connected_users.append((user.id, user.email))

        if (current_user.id == sent_connections_tmp[i].user_id_recieves and
                sent_connections_tmp[i].are_connected is False):
            user = User.query.filter_by(id=sent_connections_tmp[i].user_id_sends).first()
            incoming_reqs.append((user.id, user.email))

    return render_template('account.html', title='Account', pdf_file=pdf_file,
                            post=post, sent_connections=sent_connections,
                            sent_connections_num=sent_connections_num,
                            connected_users=connected_users,
                            incoming_reqs=incoming_reqs)


@users.route('/account', methods=['POST'])
@login_required
def update_account():
    # checks if the user with the same username already exists
    if request.form['email']:
        if User.query.filter_by(email=request.form['email']).first() is not None:
            flash('Username already exists!', 'error')
            return redirect(url_for('users.account'))
        else:
            current_user.email = request.form['email']

    if request.files['file']:
        current_user.user_uploaded_file = update_file(request.files['file'])

    if request.form['email'] or request.files['file']:
        db.session.commit()
    flash('Success!', 'success')
    return redirect(url_for('users.account'))


@users.route('/upload_cv', methods=['POST'])
@login_required
def upload_cv():
    # Check whether uploaded CV has the right extension and save it
    if request.files['file']:
        current_user.user_uploaded_file = update_file(request.files['file'])
        db.session.commit()
        flash('Success!', 'success')
    return render_template('processing_upl_cv.html', title='Processing...')


@users.route('/users_connect')
def users_connect():
    url = request.referrer
    user_id_from_url = int(re.findall(r'\d+', url)[-1])  # finds the last digit in previous url
    connection = Connections(user_id_sends=current_user.id, user_id_recieves=user_id_from_url,
                            are_connected=False)
    db.session.add(connection)
    db.session.commit()
    flash('Success', 'success')
    return redirect(url_for('posts.get_specific_post', post_id=user_id_from_url))


@users.route('/users_disconnect', methods=['POST'])
def users_disconnect():
    url = request.referrer
    user_id_from_url = int(re.findall(r'\d+', url)[-1])  # finds the last digit in previous url
    connection_first = Connections.query\
                    .filter_by(user_id_sends=current_user.id,
                                user_id_recieves=user_id_from_url)\
                    .first()
    connection_second = Connections.query\
                    .filter_by(user_id_sends=user_id_from_url,
                                user_id_recieves=current_user.id)\
                    .first()
    if connection_first is None:
        db.session.delete(connection_second)
        db.session.commit()
    elif connection_second is None:
        db.session.delete(connection_first)
        db.session.commit()
    flash('Success', 'success')
    return redirect(url_for('posts.get_specific_post', post_id=user_id_from_url))


@users.route('/accept_connection/<int:sender_id>', methods=['POST'])
def accept_connection(sender_id):
    incoming_connection = Connections.query\
        .filter_by(user_id_sends=sender_id, user_id_recieves=current_user.id)\
        .first()
    incoming_connection.are_connected = True
    db.session.commit()
    flash('Success', 'success')
    return redirect(url_for('users.account'))


@users.route('/refuse_connection/<int:sender_id>', methods=['POST'])
def refuse_connection(sender_id):
    incoming_connection = Connections.query\
        .filter_by(user_id_sends=sender_id, user_id_recieves=current_user.id)\
        .first()
    db.session.delete(incoming_connection)
    db.session.commit()
    flash('Success', 'success')
    return redirect(url_for('users.account'))


@users.route('/query_all')
@auth.login_required
def query_all():
    users = User.query.all()
    posts = ProcessedFile.query.all()
    connections = Connections.query.all()
    return f"<p>{users}</p><br><p>{posts}</p><br><p>{connections}</p><br>"
