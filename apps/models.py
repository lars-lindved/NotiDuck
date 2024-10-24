# apps/models.py

from flask_login import UserMixin
from apps import db, login_manager
from apps.authentication.util import hash_pass


class User(db.Model, UserMixin):
    __tablename__ = 'users'  # Table name in lowercase
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = hash_pass(password)

    def __repr__(self):
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class NewsletterSubscriber(db.Model):
    __tablename__ = 'newsletter_subscribers'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subscribed_on = db.Column(db.DateTime, nullable=False, default=db.func.now())

    def __repr__(self):
        return f'<NewsletterSubscriber {self.email}>'
