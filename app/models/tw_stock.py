from utils.config import db 
import uuid
import datetime

class BaseModel():
    __table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8', 'mysql_collate':'utf8_general_ci'}

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Invalid parameter {key}")

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class TWStock(BaseModel, db.Model):
    __tablename__ = 'tw_stock'

    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    number = db.Column(db.String(36), unique=True, nullable=False, index=True)
    name = db.Column(db.String(36), unique=True, nullable=False, index=True)
    stock_prices = db.relationship("TWStockPrices")

class TWStockPrices(BaseModel, db.Model):
    __tablename__ = 'tw_stock_prices'

    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    stock_id = db.Column(db.String(36), db.ForeignKey('tw_stock.id', ondelete='cascade'), nullable=True)
    price_type = db.Column(db.Integer, nullable=False)
    opening_price = db.Column(db.FLOAT(precision=10, decimal_return_scale=2))
    closing_price = db.Column(db.FLOAT(precision=10, decimal_return_scale=2))
    bid_price = db.Column(db.FLOAT(precision=10, decimal_return_scale=2))
    ask_price = db.Column(db.FLOAT(precision=10, decimal_return_scale=2))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow, index=True)
