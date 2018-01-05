'''
# app.py
'''
import sys
from flask import Flask, jsonify, request, url_for
from models import db, Product
from schemas import ma, product_schema, products_schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory"
db.init_app(app)
ma.init_app(app)

@app.route("/products/<int:id>")
def get_product(id):
    product = Product.query.get_or_404(id)
    return product_schema.jsonify(product)

@app.route("/products/", methods=["GET"])
def list_products():
    all_products = Product.query.all()
    return products_schema.jsonify(all_products)

@app.route("/products/", methods=["POST"])
def create_product():
    print("Inside create_product")
    print(request)
    print(jsonify(request.form))
    product, errors = product_schema.load(request.get_json())
    print(product)
    print(errors)
    if errors:
        resp = jsonify(errors)
        resp.status_code = 400
        return resp
    db.session.add(product)
    db.session.commit()

    resp = jsonify({"message":"created"})
    resp.status_code = 201
    resp.headers["Location"] = product.url
    return resp

@app.route("/products/<int:id>", methods=["POST"])
def edit_product(id):
    product = Product.query.get_or_404(id)
    product, errors = product_schema.load(request.get_json(), instance=product)
    if errors:
        resp = jsonify(errors)
        resp.status_code = 400
        return resp

    db.session.add(product)
    db.session.commit()
    
    resp = jsonify({"message":"updated"})
    return resp

@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message":"deleted"})

# @app.route("/<slug>")
# def get_product(slug):
#     product = session.query(Product).filter(Product.slug == slug).first()
#     if product == None:
#         abort(404)
#     return product_schema.jsonify(product)

@app.errorhandler(404)
def page_not_found(error):
    resp = jsonify({"error":"not found"})
    resp.status_code = 404
    return resp

if __name__ == "__main__":
    if "createdb" in sys.argv:
        with app.app_context():
            db.create_all()
        print("Database Created! ...")
    elif "seeddb" in sys.argv:
        with app.app_context():
            p1 = Product(slug="sku1", name="Television", image_url="")
            db.session.add(p1)
            p2 = Product(slug="sku2", name="Computer", image_url="")
            db.session.add(p2)
            db.session.commit()
        print("Database seeded...")
    else:
        app.run(debug=True)
