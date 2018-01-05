from flask_marshmallow import Marshmallow

from models import Product

ma = Marshmallow()

class ProductSchema(ma.ModelSchema):
    class Meta:
        model = Product

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)