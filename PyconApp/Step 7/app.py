'''
# app.py
'''
import sys
from flask import Flask, jsonify, abort
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from models import Product, Base

app = Flask(__name__)
engine = create_engine('sqlite:///:memory', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

@app.route("/<slug>")
def get_product(slug):
    product = session.query(Product).filter(Product.slug == slug).first()
    if product == None:
        abort(404)
    output = {
        "name": product.name,
        "image_url": product.image_url
    }
    return jsonify(output)


if __name__ == "__main__":
    if "createdb" in sys.argv:
        with app.app_context():
            Base.metadata.create_all(engine)        
        print("Database Created! ...")
    elif "seeddb" in sys.argv:
        with app.app_context():
            p1 = Product(slug="sku1", name="Television", image_url="")
            session.add(p1)
            p2 = Product(slug="sku2", name="Computer", image_url="")
            session.add(p2)
            session.commit()
        print("Database seeded...")
    else:
        app.run(debug=True)
