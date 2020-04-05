import enum

from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    count = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Order {}>'.format(self.product)


class Roles(enum.Enum):
    Reader = 'reader'
    Admin = 'admin'


class Rangs(enum.Enum):
    Bronze = 'bronze'
    Silver = 'silver'
    Gold = 'gold'
    Platina = 'platina'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    bank = db.Column(db.Integer, default=0)
    rang = db.Column(db.Enum(Rangs), default=None)
    role = db.Column(db.Enum(Roles), default=Roles.Reader)
    orders = db.relationship('Order', backref='customer', lazy='dynamic')

    def is_admin(self):
        return self.role == Roles.Admin

    def set_rang(self, rang):
        self.rang = rang
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(64), index=True, nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturer.id'), nullable=False)
    count = db.Column(db.Integer, default=0)
    price = db.Column(db.Integer, nullable=False)
    orders = db.relationship('Order', backref='product', lazy='dynamic')

    def __repr__(self):
        return '<Product {}>'.format(self.model)


class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    products = db.relationship('Product', backref='type', lazy='dynamic')

    def __repr__(self):
        return '<Produc type {}>'.format(self.name)


class Manufacturer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    products = db.relationship('Product', backref='manufacturer', lazy='dynamic')
    ambassador = db.Column(db.String(64), nullable=False)