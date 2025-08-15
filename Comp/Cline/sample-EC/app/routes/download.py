from flask import Blueprint, send_file, abort
from flask_login import login_required, current_user
from app.models import OrderItem, Order, Product

download_bp = Blueprint('download', __name__)

@download_bp.route('/download/<int:order_item_id>')
@login_required
def download_pdf(order_item_id):
    order_item = OrderItem.query.get_or_404(order_item_id)
    order = Order.query.get(order_item.order_id)
    if order.user_id != current_user.id:
        abort(403)
    product = Product.query.get(order_item.product_id)
    if not product or not product.pdf_file:
        abort(404)
    return send_file(product.pdf_file, as_attachment=True)
