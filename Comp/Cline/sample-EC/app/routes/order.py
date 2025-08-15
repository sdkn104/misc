from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Cart, CartItem, Product, Order, OrderItem, db
from datetime import datetime

order_bp = Blueprint('order', __name__)

@order_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    items = []
    total = 0
    if cart:
        items = CartItem.query.filter_by(cart_id=cart.id).all()
        for item in items:
            product = Product.query.get(item.product_id)
            total += product.price * item.quantity
    if request.method == 'POST':
        # 決済処理（仮）: 実際は外部API連携等
        order = Order(
            user_id=current_user.id,
            created_at=datetime.now(),
            total_price=total
        )
        db.session.add(order)
        db.session.commit()
        for item in items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity
            )
            db.session.add(order_item)
        # カートを空にする
        CartItem.query.filter_by(cart_id=cart.id).delete()
        db.session.commit()
        flash('購入が完了しました。')
        return redirect(url_for('order.order_complete', order_id=order.id))
    return render_template('checkout.html', items=items, total=total)

@order_bp.route('/order/complete/<int:order_id>')
@login_required
def order_complete(order_id):
    order = Order.query.get_or_404(order_id)
    # ダウンロードURL生成は後で追加
    return render_template('order_complete.html', order=order)

@order_bp.route('/orders')
@login_required
def order_history():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('order_history.html', orders=orders)
