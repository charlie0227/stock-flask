from utils.config import db 
from models.enums import StockType
import uuid
import datetime
from sqlalchemy import UniqueConstraint

class BaseModel():
    __table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8', 'mysql_collate':'utf8_general_ci'}

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Invalid parameter: {key}")

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class TWStock(BaseModel, db.Model):
    __tablename__ = 'tw_stock'

    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    number = db.Column(db.String(36), unique=True, nullable=False, index=True)
    name = db.Column(db.String(36), unique=True, nullable=False, index=True)
    stock_price_daily = db.relationship("TWStockPriceDaily", backref="stock")

class TWStockPrice(BaseModel, db.Model):
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    price_type = db.Column(db.Enum(StockType))
    transactions_number = db.Column(db.BigInteger)
    transactions_price = db.Column(db.BigInteger)
    opening_price = db.Column(db.FLOAT(precision=10, decimal_return_scale=2))
    closing_price = db.Column(db.FLOAT(precision=10, decimal_return_scale=2))
    high_price = db.Column(db.FLOAT(precision=10, decimal_return_scale=2))
    low_price = db.Column(db.FLOAT(precision=10, decimal_return_scale=2))
    date = db.Column(db.DateTime, index=True)
    created_time = db.Column(db.DateTime, default=datetime.datetime.utcnow, index=True)

    UniqueConstraint('stock_id', 'date')

class TWStockPriceDaily(TWStockPrice):
    __tablename__ = 'tw_stock_price_daily'
    stock_number = db.Column(db.String(36), db.ForeignKey('tw_stock.number', ondelete='cascade'), nullable=True)
    
    def as_dict(self):
        base = super().as_dict()
        base["price_type"] = base["price_type"].name
        base["date"] = base["date"].strftime('%Y-%m-%d %H:%M:%S')
        base["created_time"] = base["created_time"].strftime('%Y-%m-%d %H:%M:%S')
        base["stock_id"] = self.stock.id
        base["stock_name"] = self.stock.name
        return base