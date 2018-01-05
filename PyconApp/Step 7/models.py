from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence

Base = declarative_base()

class Product(Base):
    __tablename__ = 'product'

    product_id = Column(Integer, Sequence('product_id_seq'), primary_key=True)
    slug = Column(String(64), index=True)
    name = Column(String(64), nullable=False)
    image_url = Column(String(128), nullable=True)

    def __repr__(self):
        return "<Product(id='%s',slug='%s',name='%s',image_url='%s')>" % (
                                self.product_id,self.slug,self.name,self.image_url)


