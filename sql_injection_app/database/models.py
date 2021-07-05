from flask_login import UserMixin
from sql_injection_app import db
from werkzeug.security import generate_password_hash, check_password_hash


class authentication(UserMixin, db.Model):
    __tablename__ = 'authentication'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Integer, nullable=False)

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role


class product(UserMixin, db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, index=True, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, name, price):
        self.name = name
        self.price = price
