from .database import db
from flask import Blueprint,render_template, redirect, url_for, request, jsonify
from flask import current_app as app
from flask_login import login_user, login_required, logout_user, current_user
from application.models import User, Product, Orders, Cart, Category, Sales
from application.forms import SearchForm, RegisterForm, LoginForm, AddCategory, AddProduct
from datetime import datetime
from application import bcrypt

unit_list = ["Rs./kg", "Rs./g", "Rs./lb", "Rs./oz", "Rs./L", "Rs./mL", "Rs./dozen", "Rs./unit", "Rs./piece", "Rs./pack", "Rs./bag", "Rs./box", "Rs./bundle", "Rs./bunch", "Rs./can", "Rs./jar", "Rs./packet", "Rs./container", "Rs./carton", "Rs./slice", "Rs./cup", "Rs./pint", "Rs./quart", "Rs./liter", "Rs./milliliter", "Rs./fluid ounce"]

app = Blueprint('main', __name__)

@app.context_processor
def base():
    form = SearchForm()
    category = Category.query.all()
    return dict(form = form, category = category)

@app.route('/')
def home():
    return render_template('index.html')

@app.errorhandler(404)
def not_found(error):
    resp = jsonify({'error':'not found'})
    resp.status_code = 404
    return resp

@app.route('/register', methods = ['POST', 'GET'])
def register():
    now = datetime.now()
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data,email = form.email.data, password=hashed_password, full_name=form.full_name.data, gender=form.gender.data,dob = form.dob.data, phone_no=form.phone_no.data, created_at=now)
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            return redirect(url_for('main.register'))
        return redirect(url_for('main.login'))


    return render_template('register.html', form = form)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()       
        if user and user.user_id != 1:
            if bcrypt.check_password_hash(pw_hash=user.password, password=form.password.data):
                login_user(user)
                return redirect(url_for('main.dashboard'))
        elif user and user.user_id == 1:
            print(Exception("Invalid User Login"))
    alt_login = "Admin Login"
    href = "admin_login"
    return render_template('login.html', form = form, authentication = "Login", alt_login=alt_login, href = href)

@app.route('/admin_login', methods = ['POST', 'GET'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = User.query.filter_by(username=form.username.data).first()
        print(form.username.data)
        if admin and admin.user_id == 1:
            if bcrypt.check_password_hash(admin.password, form.password.data):
                login_user(admin)
                return redirect(url_for('main.admin'))
        elif admin and admin.user_id != 1:
            print(Exception("Invalid Admin Login"))
    alt_login = "User Login"
    href = "login"
    return render_template('login.html', form = form, authentication = "Admin Login", alt_login = alt_login, href = href)


@app.route('/admin', methods = ['GET'])
@login_required
def admin():
    form = SearchForm()
    products = db.session.query(Product, Category).join(Category, Product.category_id == Category.category_id).all()
    category_list = Category.query.all()
    return render_template('admin.html', form=form, products=products, cat_list = category_list)

@app.route('/admin/add_category', methods = ['POST', 'GET', 'DELETE', 'PUT'])
@login_required
def add_category():
    now = datetime.now()
    category_form = AddCategory()
    if category_form.validate_on_submit():
        new_category = Category(name = category_form.name.data.lower().strip(), created_at = now)
        db.session.add(new_category)
        try:
            db.session.commit()
            return redirect(url_for('main.admin'))
        except Exception as e:
            print(e)
            return redirect(url_for('main.admin'))
    
    return render_template('add_category.html', cat_form = category_form)

@app.route('/admin/add_product', methods = ['POST', 'GET', 'DELETE', 'PUT'])
@login_required
def add_product():
    
    now = datetime.now()
    product_form = AddProduct()
    category_list = Category.query.all()
    if product_form.validate_on_submit():
        new_category = Product(name = product_form.name.data,description = product_form.description.data,
                               price = product_form.price.data, unit = product_form.unit.data, stock_quantity = product_form.stock_quantity.data,
                               manufacture_date = product_form.manufacture_date.data, expiry_date = product_form.expiry_date.data,
                               created_at = now, category_id = Category.query.filter_by(name=product_form.category_name.data).first().category_id)
        db.session.add(new_category)
        try:
            db.session.commit()
            return redirect(url_for('main.admin'))

        except Exception as e:
            print(e)
            return redirect(url_for('main.admin'))
    return render_template('add_product.html', prod_form = product_form, category_list = category_list, unit_list = unit_list)

@app.route('/admin/edit_category/<cat_id>', methods=['GET','POST'])
@login_required
def edit_category(cat_id):
    now = datetime.now()
    category = Category.query.filter_by(category_id=cat_id).first()
    category_form = AddCategory()
    if category_form.validate_on_submit():
        db.session.query(Category).filter(Category.category_id == cat_id).update({'name': category_form.name.data, 'created_at' : now})
    
        try:
            db.session.commit()
            return redirect(url_for('main.admin'))
        except Exception as e:
            print(e)
            return redirect(url_for('main.admin'))
    return render_template('edit_category.html', cat_form = category_form, category = category)

@app.route('/admin/edit_product/<prod_id>', methods=['GET','POST'])
@login_required
def edit_product(prod_id):
    now = datetime.now()
    product = Product.query.filter_by(product_id=prod_id).first()
    product_form = AddProduct()
    category_list = Category.query.all()
    if product_form.validate_on_submit():
        db.session.query(Product).filter(Product.product_id == prod_id).update({'name': product_form.name.data,'description': product_form.description.data,
                               'price' : product_form.price.data, 'unit' : product_form.unit.data, 'stock_quantity' : product_form.stock_quantity.data,
                               'manufacture_date' : product_form.manufacture_date.data, 'expiry_date' : product_form.expiry_date.data,
                               'created_at' : now, 'category_id' : Category.query.filter_by(name=product_form.category_name.data).first().category_id})
    
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            return redirect(url_for('main.admin'))
    return render_template('edit_product.html', prod_form = product_form, cat_list = category_list, unit_list = unit_list, product = product)
    

@app.route('/admin/remove_product/<prod_id>', methods=['POST','GET', 'DELETE'])
@login_required
def remove_product(prod_id):
    db.session.query(Product).filter(Product.product_id == prod_id).delete()
    try:
        db.session.commit()
    except Exception as e:
        print(e)
    return redirect(url_for('main.admin'))

@app.route('/admin/remove_category/<cat_id>', methods=['POST','GET', 'DELETE'])
@login_required
def remove_category(cat_id):
    db.session.query(Product).filter_by(category_id = cat_id).delete()
    db.session.query(Category).filter(Category.category_id == cat_id).delete()
    try:
        db.session.commit()
        print("hellp")
    except Exception as e:
        print(e)
    return redirect(url_for('main.admin'))
    
@app.route('/logout', methods = ['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@app.route('/search', methods = ['GET', 'POST'])
def search():
    form  = SearchForm()
    products = Product.query
    categories = Category.query.all()
    if form.validate_on_submit():
        searched = form.search.data

        searched_products = db.session.query(Product, Category).join(Category, Product.category_id == Category.category_id).filter(Product.name.like('%'+searched+'%')).order_by(Product.name).all()
        searched_category = db.session.query(Category).filter(Category.name.like('%'+searched+'%')).order_by(Category.name).all()
        print(searched_products)
        return render_template('search.html', form = form, searched = searched, items = searched_products, cate = searched_category, category = categories)

@app.route('/admin_search', methods = ['GET', 'POST'])
def adminsearch():
    form  = SearchForm()
    products = Product.query
    categories = Category.query.all()
    if form.validate_on_submit():
        searched = form.search.data

        searched_products = db.session.query(Product, Category).join(Category, Product.category_id == Category.category_id).filter(Product.name.like('%'+searched+'%')).order_by(Product.name).all()
        searched_category = db.session.query(Category).filter(Category.name.like('%'+searched+'%')).order_by(Category.name).all()

        return render_template('admin_search.html', form = form, searched = searched, items = searched_products, cate = searched_category, category = categories)

@app.route('/dashboard', methods = ['GET','POST'])
@login_required
def dashboard():
    form = SearchForm()
    category = Category.query.all()
    cart_price = 0
    cart_items = db.session.query(Cart, Product).join(Product, Cart.product_id == Product.product_id and Cart.user_id == current_user.user_id).filter(Cart.user_id == current_user.user_id).all()
    order_items = db.session.query(Orders, Product).join(Product, Orders.product_id == Product.product_id and Orders.user_id == current_user.user_id).filter(Orders.user_id == current_user.user_id).all()
    for (i,j) in cart_items:
        cart_price += j.price * i.quantity
    category_product = {}
    latest_products = db.session.query(Product, Category).join(Category, Product.category_id == Category.category_id).order_by(Product.product_id.desc()).limit(12)
    products = db.session.query(Product, Category).join(Category, Product.category_id == Category.category_id).all()
    for j in products:
        if j[1].name in category_product:
            category_product[j[1].name].append(j[0])
        else:
            category_product[j[1].name] = []
            category_product[j[1].name].append(j[0])
    for i in category_product:
        print(i)
            
    return render_template('dashboard.html', form = form, latest_products = latest_products, category = category, cat_pro = category_product, user = current_user, cart_items = cart_items, order_items = order_items, cart_price = cart_price)

@app.route('/add_to_cart/', methods = ['GET','POST'])
@login_required
def add_to_cart():
    now = datetime.now()
    product_id = request.args.get('product_id', None)
    quantity = request.args.get('quantity', None)
    item_exist = db.session.query(Cart).filter((Cart.product_id==product_id) and (Cart.user_id==current_user.user_id)).first()
    if not item_exist:
        new_product = Cart(product_id=product_id, user_id=current_user.user_id, quantity = quantity, created_at = now)
    try:
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('main.dashboard'))
    except Exception as e:
        print(e)
        db.session.rollback()
        return redirect(url_for('main.dashboard'))

@app.route('/remove_cart/<product_id>', methods = ['POST', 'GET'])
@login_required
def remove_cart(product_id):
    try:
        db.session.query(Cart).filter((Cart.product_id==product_id) and (Cart.user_id == current_user.user_id)).delete()
        db.session.commit()
    except Exception as e:
        print(e)
    return redirect(url_for('main.dashboard'))

def insert_into_sales(order, session):
    # Replace these attributes with actual attributes based on your application
    now = datetime.now()

    # Create a new Sale entry
    sale = Sales(
        order_id=order.order_id,
        product_id=order.product_id,
        quantity=order.quantity,
        created_at = now
    )
    session.add(sale)
    session.commit()
    return 

def delete_product_from_cart(product_id, session):
    try:
        # Attempt to delete the product from the cart
        session.query(Cart).filter(Cart.product_id == product_id).delete()
        session.commit()
        print("Product removed from the cart.")
    except Exception as e:
        # Handle other exceptions that might occur during the deletion process
        session.rollback()
        print(e)
    return 

@app.route('/empty_cart', methods=['POST', 'GET'])
@login_required
def empty_cart():
    now = datetime.now()
    try:
        # Delete all rows from the Cart table where Cart.user_id == current_user.user_id
        db.session.query(Cart).filter(Cart.user_id == current_user.user_id).delete()
        db.session.commit()
        print("Cart emptied successfully.")
    except Exception as e:
        db.session.rollback()
        print("Error emptying cart:", e)
        return redirect(url_for('main.dashboard'))

    # Redirect back to the dashboard
    return redirect(url_for('main.dashboard'))



@app.route('/checkin_cart', methods=['POST', 'GET'])
@login_required
def checkin_cart():
    now = datetime.now()
    product_id = request.args.get('product_id', None)
    quantity = request.args.get('quantity', None)
    
    try:
        if product_id is not None and quantity is not None:
            new_order = Orders(user_id = current_user.user_id, product_id = product_id, quantity = quantity, created_at = now)
            db.session.add(new_order)
            db.session.commit()
            order = db.session.query(Orders).get(new_order.order_id)
            product = db.session.query(Product).get(product_id)
            print(Product)
            if product:
                product.stock_quantity -= quantity
            insert_into_sales(order, db.session)
            db.session.commit()
        
        else: 
            cart_items = db.session.query(Cart, Product).join(Product, Cart.product_id == Product.product_id and Cart.user_id == current_user.user_id).all()
            for (i,j) in cart_items:
                new_order = Orders(user_id = current_user.user_id, product_id = j.product_id, quantity = i.quantity, created_at = now)
                db.session.add(new_order)
                db.session.commit()
                order = db.session.query(Orders).get(new_order.order_id)
                product = db.session.query(Product).get(j.product_id)
                if product:
                    product.stock_quantity -= i.quantity
                insert_into_sales(order, db.session)
                delete_product_from_cart(j.product_id, db.session)

            print("Order created and Sales triggered successfully.")
    except Exception as e:
        db.session.rollback()
        print(e)
        return redirect(url_for('main.dashboard'))
    finally:
        # Close the session
        db.session.close()
        return redirect(url_for('main.dashboard'))


    
