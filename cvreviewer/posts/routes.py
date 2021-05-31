import os
from flask import (Blueprint, render_template, request, redirect, 
                    url_for, abort, current_app, flash)
from flask_login import login_required, current_user
from cvreviewer.models import User, ProcessedFile, Connections
from cvreviewer.sillyname import rand_silly_name
from cvreviewer.document_reader import DocumentReader
from cvreviewer import db

posts = Blueprint('posts', __name__)


@posts.route('/post/new')
@login_required
def new_post():
    post = ProcessedFile.query.get(current_user.id)
    if post is None:
        silly_uname = rand_silly_name()
        file_path = os.path.join(current_app.root_path, current_app.config['UPLOAD_PATH'], 
                                current_user.user_uploaded_file)
        extracted_text = DocumentReader(file_path)
        return render_template('new_post.html', title='New Post', silly_uname=silly_uname,
                            extracted_text=extracted_text.tokenized_pdf)
    else:
        return render_template('post_already_exists.html', title='Your post already exists')


@posts.route('/post/new', methods=['POST'])
@login_required
def new_post_add():
    processed_cv_post = ProcessedFile(id=current_user.id,
        title=request.form['silly-uname'] + "'s CV",
        content=request.form['pdf-text'],
        entity_content=DocumentReader.displacy_entity_html(request.form['pdf-text']),
        user_id=current_user.id)
    db.session.add(processed_cv_post)
    db.session.commit()
    flash('Success!', 'success')
    return redirect(url_for('posts.get_specific_post', post_id=current_user.id))


@posts.route('/dashboard')
@login_required
def posts_dashboard():
    # query posts -> recent first
    posts = ProcessedFile.query.order_by(ProcessedFile.date_processed.desc()).all()
    return render_template('posts_dashboard.html', title='Posts Dashboard', posts=posts)


@posts.route('/post/<int:post_id>')
@login_required
def get_specific_post(post_id):
    post = ProcessedFile.query.get_or_404(post_id)
    connections_sender = Connections.query.filter_by(user_id_sends=current_user.id).first()
    connections_reciever = Connections.query.filter_by(user_id_recieves=current_user.id).first()
    user_connected = User.query.filter_by(id=post_id).first()
    pdf_file = url_for('static', filename='uploads/' + user_connected.user_uploaded_file)
    return render_template('post.html', title=post.title, post=post,
                            connections_sender=connections_sender,
                            connections_reciever=connections_reciever,
                            user_connected=user_connected,
                            pdf_file=pdf_file)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_specific_post(post_id):
    post = ProcessedFile.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    if request.method == 'POST':
        post.title = request.form['silly-uname']
        post.content = request.form['pdf-text']
        post.entity_content = DocumentReader.displacy_entity_html(request.form['pdf-text'])
        db.session.commit()
        flash('Success!', 'success')
        return redirect(url_for('posts.get_specific_post', post_id=post.id))
    return render_template('update_post.html', title='Update Post', post=post)


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_specific_post(post_id):
    post = ProcessedFile.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Success!', 'success')
    return redirect(url_for('posts.posts_dashboard'))
