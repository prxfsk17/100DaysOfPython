import os
import stripe
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_demo')
stripe_public_key = os.environ.get('STRIPE_PUBLIC_KEY', 'pk_test_demo')

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    stock = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.now())

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20))
    address = db.Column(db.Text, nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, paid, completed
    stripe_payment_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.now)

with app.app_context():
    db.create_all()

    if Product.query.count() == 0:
        test_product = Product(
            name="test product",
            price=100.00,
            description="description of test product",
            image_url="https://images.unsplash.com/photo-1598128558393-70ff21433be0?q=80&w=789&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            stock=10
        )
        db.session.add(test_product)
        db.session.commit()

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products, stripe_public_key=stripe_public_key)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    product_id_str = str(product_id)
    cart[product_id_str] = cart.get(product_id_str, 0) + 1

    session.modified = True
    flash('Product added to cart!', 'success')
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    cart_items = []
    total = 0

    if 'cart' in session:
        for product_id_str, quantity in session['cart'].items():
            product = Product.query.get(int(product_id_str))
            if product:
                item_total = product.price * quantity
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'total': item_total
                })
                total += item_total

    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if 'cart' in session:
        session['cart'].pop(str(product_id), None)
        session.modified = True
        flash('Product deleted from cart', 'info')

    return redirect(url_for('cart'))


@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session.pop('cart', None)
    flash('Cart cleared', 'info')
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'GET':
        cart_items = []
        total = 0

        if 'cart' in session:
            for product_id_str, quantity in session['cart'].items():
                product = Product.query.get(int(product_id_str))
                if product:
                    item_total = product.price * quantity
                    cart_items.append({
                        'product': product,
                        'quantity': quantity,
                        'total': item_total
                    })
                    total += item_total

        if not cart_items:
            flash('Cart is empty', 'error')
            return redirect(url_for('cart'))

        return render_template('checkout.html', cart_items=cart_items, total=total)

    if 'cart' not in session or not session['cart']:
        flash('Cart is empty', 'error')
        return redirect(url_for('cart'))

    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    address = request.form.get('address')

    if not all([name, email, address]):
        flash('Please fill all necessary fields', 'error')
        return redirect(url_for('checkout'))

    total = 0
    cart_items = []

    for product_id_str, quantity in session['cart'].items():
        product = Product.query.get(int(product_id_str))
        if product:
            total += product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity
            })

    try:
        order = Order(
            customer_name=name,
            customer_email=email,
            customer_phone=phone,
            address=address,
            total=total
        )
        db.session.add(order)
        db.session.commit()

        try:
            if stripe_public_key.startswith('pk_test_'):
                payment_intent = stripe.PaymentIntent.create(
                    amount=int(total * 100),
                    currency='eur',
                    metadata={'order_id': order.id},
                    description=f"Order #{order.id}"
                )

                order.stripe_payment_id = payment_intent['id']
                db.session.commit()

                return render_template('checkout.html',
                                       order=order,
                                       client_secret=payment_intent.client_secret,
                                       stripe_public_key=stripe_public_key)
            else:
                flash('Ordered successfully!', 'success')
                session.pop('cart', None)
                return redirect(url_for('order_success', order_id=order.id))

        except Exception as e:
            flash(f'Error with creating order: {str(e)}', 'error')
            return redirect(url_for('checkout'))

    except Exception as e:
        flash(f'Error with order checkout: {str(e)}', 'error')
        return redirect(url_for('checkout'))


@app.route('/order/success/<int:order_id>')
def order_success(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('success.html', order=order)

if __name__ == '__main__':
    print("Stripe's test cards:")
    print("   4242 4242 4242 4242 - успешный платеж")
    print("   4000 0000 0000 9995 - недостаточно средств")
    print("   4000 0000 0000 0002 - карта отклонена")
    app.run(debug=True, port=5000)