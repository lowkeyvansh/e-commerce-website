from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(100), nullable=False)

db.create_all()

@app.route('/')
def home():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/product/<int:id>')
def product(id):
    product = Product.query.get_or_404(id)
    return render_template('product.html', product=product)

@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(id)
    return redirect(url_for('home'))

@app.route('/cart')
def cart():
    if 'cart' not in session:
        return redirect(url_for('home'))
    cart_items = [Product.query.get_or_404(id) for id in session['cart']]
    total = sum(item.price for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/checkout')
def checkout():
    if 'cart' not in session:
        return redirect(url_for('home'))
    session.pop('cart', None)
    return render_template('checkout.html')

if __name__ == '__main__':
    app.run(debug=True)
