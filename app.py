from flask import Flask, render_template, request, redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
db = SQLAlchemy(app)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(precision=8, scale=2), nullable=False)
    image = db.Column(db.String(100))
    category = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    stock = db.Column(db.Integer, nullable=False)



@app.route("/product")
@app.route("/product/<id>")
def product(id=-1):
    if id == -1:
        products = Product.query.all()
    else:
        products = [Product.query.get(id)]
    return_data = []
    for product in products:
        return_data.append(
            {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'image': product.image,
                'category': product.category,
                'stock': product.stock
            })
    if id != -1:
        return jsonify(return_data[0])

    return jsonify(return_data)



@app.route("/add_product", methods=["POST"])
@app.route("/add_product/<id>", methods=["POST","GET"])
def add_product(id=-1):
    if request.method == "POST":
        name = request.get_json().get("name")
        price = request.get_json().get("price")
        image = request.get_json().get("image")
        category = request.get_json().get("category")
        stock = request.get_json().get("stock")
        print(f"!!! {name},{price},{image},{category},{stock}")
        # add new product
        if id == -1:
            product = Product(name=name, price=price,
                              image=image, category=category, stock=stock)
            db.session.add(product)
            db.session.commit()
        else:
            product = Product.query.get(id)
            product = Product(name=name, price=price,
                            image=image, category=category, stock=stock)
            db.session.commit()
        response = {'message': 'POST request received successfully'}    
        return jsonify(response)
    else:
        product = Product.query.get(id)
        response = {
            'id': product.id,
                'name': product.name,
                'price': product.price,
                'image': product.image,
                'category': product.category,
                'stock': product.stock 
        }
        print(f"*******{response}*******")
        return jsonify(response)
    


@app.route("/delete_product/<id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
        response = {'message': 'POST request received successfully'}    
        return jsonify(response)
    else:
        return jsonify({'error': 'product not found'})
    

@app.route("/category")
def category():
    categorys = Category.query.all()
    return_data = []
    for category in categorys:
        return_data.append(
            {
                'id': category.id,
                'name': category.name,
            })

    return jsonify(return_data)


@app.route("/add_category", methods=["POST"])
def add_category():

    name = request.get_json().get("name")

    print(f"!!!category - {name} !!!")
    # add new category

    new_category = Category(name=name)
    db.session.add(new_category)
    db.session.commit()
        

    response = {'message': 'POST request received successfully'}
    return jsonify(response)






with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
