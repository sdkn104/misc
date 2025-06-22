import os
from flask import Flask, render_template, redirect, url_for, request, flash, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'devkey')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql://user:password@localhost/pdf_ec')
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static', 'pdfs')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from models import User, Product, Cart, Order

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('既に登録されています')
            return redirect(url_for('register'))
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('登録完了。ログインしてください')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        flash('メールアドレスまたはパスワードが違います')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/cart')
@login_required
def cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    return render_template('cart.html', cart_items=cart_items)

@app.route('/cart/add/<int:product_id>')
@login_required
def add_to_cart(product_id):
    if not Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first():
        cart_item = Cart(user_id=current_user.id, product_id=product_id)
        db.session.add(cart_item)
        db.session.commit()
        flash('カートに追加しました')
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    if request.method == 'POST':
        # ダミー決済処理
        order = Order(user_id=current_user.id)
        db.session.add(order)
        db.session.commit()
        for item in cart_items:
            order.products.append(item.product)
            db.session.delete(item)
        db.session.commit()
        flash('購入が完了しました')
        return redirect(url_for('order_complete', order_id=order.id))
    return render_template('checkout.html', cart_items=cart_items)

@app.route('/order_complete/<int:order_id>')
@login_required
def order_complete(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order_complete.html', order=order)

@app.route('/download/<int:order_id>/<int:product_id>')
@login_required
def download_pdf(order_id, product_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('権限がありません')
        return redirect(url_for('index'))
    product = Product.query.get_or_404(product_id)
    filename = product.filename
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True)
