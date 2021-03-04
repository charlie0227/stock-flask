import json
import os
from utils.config import api, app, db
from flask_restful import Resource
from views.stock import StockList, Stock

class HelloWorld(Resource):
    def get(self):
        return {
            'message': os.getenv('DB_USER')
        }, 200

class InitDatabase(Resource):
    def get(self):
        db.create_all()
        return {
            'message': 'DONE'
        }, 200

api.add_resource(HelloWorld, '/')
api.add_resource(InitDatabase, '/init')
api.add_resource(StockList, '/stock')
api.add_resource(Stock, '/stock/<string:stock_number>')

if __name__ == '__main__':
    db.create_all()
    app.run(host="0.0.0.0", debug=True)
