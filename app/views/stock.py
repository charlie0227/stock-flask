from models.tw_stock import TWStock, TWStockPriceDaily
from utils.config import db
from utils.share import session_scope, catch_error
from utils.stock import get_tw_stock_list, get_today_tw_stock_5
from flask_restful import Resource, reqparse
import requests
from flasgger import swag_from

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
                instance = TWStock(**stock)
                db_session.add(instance)
        return { 
            'data': stock_list
        }, 200

class Stock(Resource):
    @catch_error
    def get(self, stock_number):
        with session_scope() as db_session:
            stock = db_session.query(TWStock).filter(TWStock.number == stock_number).one()
            return {
                'data': stock.as_dict()
            }, 200

class StockDaily(Resource):
    @catch_error
    def get(self, stock_number):
        with session_scope() as db_session:
            stock = db_session.query(TWStockPriceDaily).join(TWStock).filter(TWStock.number == stock_number).one()
            return {
                'data': stock.as_dict()
            }, 200

class StockListDaily(Resource):
    @catch_error
    def post(self):
        stock_list = get_today_tw_stock_5()
        with session_scope() as db_session:
            for stock in stock_list:
                instance = TWStockPriceDaily(**stock)
                db_session.add(instance)
        return { 
            'message': stock_list
        }, 200