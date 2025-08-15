from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Product, Cart, CartItem, db

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()
    item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if item:
        item.quantity += 1
    else:
        item = CartItem(cart_id=cart.id, product_id=product_id, quantity=1)
        db.session.add(item)
    db.session.commit()
    flash('カートに追加しました。')
    return redirect(url_for('product.product_detail', product_id=product_id))

@cart_bp.route('/cart')
@login_required
def view_cart():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    items = []
    total = 0
    if cart:
        items = CartItem.query.filter_by(cart_id=cart.id).all()
        for item in items:
            product = Product.query.get(item.product_id)
            item.product = product  # テンプレート用
            total += product.price * item.quantity
    return render_template('cart.html', items=items, total=total)

@cart_bp.route('/cart/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart_item(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.cart.user_id != current_user.id:
        flash('権限がありません。')
        return redirect(url_for('cart.view_cart'))
    quantity = int(request.form.get('quantity', 1))
    if quantity < 1:
        flash('数量は1以上で指定してください。')
        return redirect(url_for('cart.view_cart'))
    item.quantity = quantity
    db.session.commit()
    flash('数量を変更しました。')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/cart/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_cart_item(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.cart.user_id != current_user.id:
        flash('権限がありません。')
        return redirect(url_for('cart.view_cart'))
    db.session.delete(item)
    db.session.commit()
    flash('商品をカートから削除しました。')
    return redirect(url_for('cart.view_cart'))
