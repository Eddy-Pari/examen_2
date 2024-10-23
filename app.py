from flask import Flask, render_template, request, redirect, url_for, session


app = Flask(__name__)
app.secret_key = 'secret_key'  # Cambia esto por una clave secreta real

@app.route('/')
def index():
    products = session.get('products', [])
    return render_template('index.html', products=products)

@app.route('/add_product', methods=['POST'])
def add_product():
    if 'products' not in session:
        session['products'] = []
    
    product_id = request.form['id']
    name = request.form['name']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])
    expiration_date = request.form['expiration_date']
    category = request.form['category']

    # Verificar si el ID ya existe
    if any(product['id'] == product_id for product in session['products']):
        return redirect(url_for('index'))  # Regresar a la lista si el ID no es único
    
    # Crear el nuevo producto
    new_product = {
        'id': product_id,
        'name': name,
        'quantity': quantity,
        'price': price,
        'expiration_date': expiration_date,
        'category': category
    }
    session['products'].append(new_product)
    session.modified = True  # Asegurarse de que la sesión se guarde
    return redirect(url_for('index'))

@app.route('/edit_product/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    products = session.get('products', [])
    product = next((p for p in products if p['id'] == product_id), None)

    if request.method == 'POST':
        product['name'] = request.form['name']
        product['quantity'] = int(request.form['quantity'])
        product['price'] = float(request.form['price'])
        product['expiration_date'] = request.form['expiration_date']
        product['category'] = request.form['category']
        session.modified = True  # Asegurarse de que la sesión se guarde
        return redirect(url_for('index'))

    return render_template('edit_product.html', product=product)

@app.route('/delete_product/<product_id>')
def delete_product(product_id):
    session['products'] = [p for p in session.get('products', []) if p['id'] != product_id]
    session.modified = True  # Asegurarse de que la sesión se guarde
    return redirect(url_for('index'))

if __name__ == '_main_':
    app.run(debug=True)