from flask import url_for
from flask_sqlalchemy import SQLAlchemy

db  = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'product'

    product_id = db.Column(db.Integer, db.Sequence('product_id_seq'), primary_key=True)
    slug = db.Column(db.String(64), index=True)
    name = db.Column(db.String(64), nullable=False)
    image_url = db.Column(db.String(128), nullable=True)

    def __repr__(self):
        return "<Product(id='%s',slug='%s',name='%s',image_url='%s')>" % (
                                self.product_id,self.slug,self.name,self.image_url)

    @property
    def url(self):
        return url_for("get_product",id=self.product_id)
