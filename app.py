from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
app.app_context().push()

from models import User, Product, Location, ProductMovement


def __repr__(self):
    return f"User(id={self.id}, username='{self.username}')"


@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='Username already exists')

        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')

# Login form
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = username
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

def __repr__(self):
        return f"Movement ID: {self.movement_id}, Timestamp: {self.timestamp}, " \
               f"From: {self.from_location}, To: {self.to_location}, " \
               f"Product ID: {self.product_id}, Quantity: {self.qty}"

@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        product_id = request.form['product_id']
        product = Product(product_id=product_id)
        db.session.add(product)
        db.session.commit()
        return redirect('/products')

    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/movements', methods=['GET', 'POST'])
def movements():
    if request.method == 'POST':
        product_id = request.form['product_id']
        from_location = request.form['from_location']
        to_location = request.form['to_location']
        qty = int(request.form['qty'])

        movement = ProductMovement(product_id=product_id, from_location=from_location,
                                   to_location=to_location, qty=qty)
        db.session.add(movement)
        db.session.commit()

    movements = ProductMovement.query.all()
    return render_template('movements.html', movements=movements)

@app.route('/balance')
def balance():
    locations = Location.query.all()
    products = Product.query.all()

    balance = []
    for location in locations:
        for product in products:
            total_in = db.session.query(func.sum(ProductMovement.qty)).filter_by(product_id=product.product_id, to_location=location.location_id).scalar()
            total_out = db.session.query(func.sum(ProductMovement.qty)).filter_by(product_id=product.product_id, from_location=location.location_id).scalar()
            qty = (total_in or 0) - (total_out or 0)
            balance.append({'product': product.product_id, 'location': location.location_id, 'qty': qty})

    return render_template('balance.html', balance=balance)

@app.route('/locations', methods=['GET', 'POST'])
def locations():
    if request.method == 'POST':
        location_id = request.form['location_id']
        location = Location(location_id=location_id)
        db.session.add(location)
        db.session.commit()
    locations = Location.query.all()
    return render_template('locations.html', locations=locations)

@app.route('/products/<string:product_id>', methods=['GET', 'POST'])
def editproduct(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        product.product_id = request.form['product_id']
        db.session.commit()
        return redirect('/products')

    return render_template('editproduct.html', product=product)

#404 error
@app.errorhandler(404)
def invalid_route(e):
    return render_template('404.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)




