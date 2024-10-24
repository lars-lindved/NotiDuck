from flask_login import UserMixin
from apps import db, login_manager
from apps.authentication.util import hash_pass

class User(db.Model, UserMixin):  # Renamed to 'User' as per convention
    __tablename__ = 'users'  # Table names are typically lowercase
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]
            if property == 'password':
                value = hash_pass(value)  # Hash the password
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user
