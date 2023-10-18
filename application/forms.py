from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, FloatField, IntegerField, DateField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired, NumberRange
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from datetime import datetime
from wtforms.widgets import Input
from .models import User, Category, Product, Cart, Orders, Sales
from . import db, app

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': "username", 'type':"text", 'class': "form-control form-control-lg"})
    email = EmailField(validators=[InputRequired(), Length(min=4, max=40)], render_kw={'placeholder': "email", 'type':"email", 'class': "form-control form-control-lg"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': "password", 'type':"password", 'class': "form-control form-control-lg"})
    full_name = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': "Full Name", 'type':"text", 'class': "form-control form-control-lg"})
    gender = StringField(validators=[InputRequired(), Length(min=4, max=10)], render_kw={'placeholder': "Gender", 'type':"text", 'class': "form-control form-control-lg"})
    phone_no = StringField(validators=[InputRequired(), Length(min=4, max=14)], render_kw={'placeholder': "Phone No.", 'type':"tel", 'class': "form-control form-control-lg"})
    dob = DateField(validators=[InputRequired()] , render_kw={'class': "form-outline datepicker w-100"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()

        if existing_user_username:
            raise ValidationError("That username already exists. Please choose a different one.")
    
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': "username", "type": "text", 'class': "form-control form-control-lg"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': "password", 'type':"password", 'class': "form-control form-control-lg"})
    submit = SubmitField("Login")

class AddCategory(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=4, max=100)], render_kw={'placeholder': "Category Name",'type':"text", 'class': "form-control form-control-lg"})
    submit = SubmitField()

    def validate_category_name(self, name):
        existing_category_name = Category.query.filter_by(name=name.data).first()

        if existing_category_name:
            raise ValidationError("That category name already exists. Please choose a different one.")

class AddProduct(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=4, max=100)], render_kw={'placeholder': "Product Name",'type':"text", 'class': "form-control form-control-lg"})
    description = StringField(validators=[InputRequired(), Length(min=4, max=200)], render_kw={'placeholder': "Description",'type':"text", 'class': "form-control form-control-lg"})
    price = FloatField(validators=[InputRequired()], render_kw={'placeholder': "price",'class': "form-control form-control-lg"})
    unit = StringField(validators=[InputRequired()], render_kw={'placeholder': "Unit",'type':"text", 'class': "form-control form-control-lg"})
    manufacture_date = DateField(validators=[InputRequired()], render_kw={'class': "form-outline datepicker w-100"})
    expiry_date = DateField(validators=[InputRequired()], render_kw={'class': "form-outline datepicker w-100"})
    stock_quantity = IntegerField(validators=[InputRequired()], render_kw={'placeholder': "Quantity",'class': "form-control form-control-lg"})
    category_name= StringField(validators=[InputRequired()], render_kw={'placeholder': "Category name",'type':"text", 'class': "form-control form-control-lg"}) 

    submit = SubmitField("Add Product")

    def validate_product_name(self, name):
        existing_product_name = Product.query.filter_by(name=name.data).first()

        if existing_product_name:
            raise ValidationError("That product name already exists. Please choose a different one.")

class RemoveCategory(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=4, max=100)], render_kw={'placeholder': "Category Name"})
    submit = SubmitField("remove Category")

class SearchForm(FlaskForm):
    search = StringField(validators=[InputRequired()])
    submit = SubmitField("search")