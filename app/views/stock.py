from models.tw_stock import TWStock, TWStockPrices
from utils.config import db
from utils.share import session_scope, catch_error
from utils.stock import get_tw_stock_list
from flask_restful import Resource, reqparse
import requests

parser = reqparse.RequestParser()

class StockList(Resource):
    @catch_error
    def get(self):
        result = []
        with session_scope() as db_session:
            stocks = db_session.query(TWStock).all()
            result = [stock.as_dict() for stock in stocks]
            
        return {
            'data': result
        }, 200

    @catch_error
    def post(self):
        stock_list = get_tw_stock_list()
        with session_scope() as db_session:
            for stock in stock_list:
                instance = TWStock(name=stock["name"], number=stock["number"])
                db_session.add(instance)
        return { 
            'data': stock_list
        }, 200

class Stock(Resource):
    @catch_error
    def get(self, stock_number):
        return {
            'message': 'Hello Wrold!'
        }, 200