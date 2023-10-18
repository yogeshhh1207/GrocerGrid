from flask_login import UserMixin
from .database import db

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    phone_no = db.Column(db.String, nullable=False, unique=True)
    dob = db.Column(db.DateTime, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False)

    def get_id(self):
           return (self.user_id)

class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False)

    def get_id(self):
        return (self.category_id)

class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float(10, 2), nullable=False)
    unit = db.Column(db.String(), nullable=False)
    stock_quantity = db.Column(db.INTEGER, nullable=False)
    manufacture_date = db.Column(db.String(), nullable=False)
    expiry_date = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))
    category = db.relationship(Category)

    def get_id(self):
        return (self.product_id)

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id') ,nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    user = db.relationship("User")
    Product = db.relationship("Product")

class Orders(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    user = db.relationship("User")
    Product = db.relationship("Product")

class Sales(db.Model):
    sale_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    order = db.relationship("Orders")
    Product = db.relationship("Product")