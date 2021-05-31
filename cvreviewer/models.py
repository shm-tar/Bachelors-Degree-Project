from datetime import datetime
from cvreviewer import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    user_uploaded_file = db.Column(db.String(20), nullable=False, default='default.pdf')
    processed_file = db.relationship('ProcessedFile', lazy=True)

    def __repr__(self):
        return f"User ('{self.id}, {self.email}', '{self.user_uploaded_file}')"


class ProcessedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    date_processed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    entity_content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Processed File ('{self.title}', '{self.date_processed}', 'Author: {self.user_id})"


class Connections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id_sends = db.Column(db.Integer, nullable=False)
    user_id_recieves = db.Column(db.Integer, nullable=False)
    are_connected = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return (f"Connection ('#{self.id}, '{self.user_id_sends}', " +
                            f"'{self.user_id_recieves}', '{self.are_connected}')")
