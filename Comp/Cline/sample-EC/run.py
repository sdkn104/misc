from app import create_app

app = create_app()

from flask import render_template
from app.models import Product

@app.route('/')
def index():
    products = Product.query.limit(5).all()  # おすすめ商品（例: 5件）
    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True, port=8888)
