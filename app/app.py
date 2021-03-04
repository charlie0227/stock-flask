import json
import os
from utils.config import api, app, db, swagger
from flask_restful import Resource
from views.stock import StockList, Stock, StockDaily, StockListDaily
from flask import redirect, request

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

@app.before_request
def clear_trailing():

    rp = request.path 
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])

if __name__ == '__main__':
    db.create_all()

    api.add_resource(HelloWorld, '/')
    api.add_resource(InitDatabase, '/init')
    api.add_resource(StockList, '/stock')
    api.add_resource(Stock, '/stock/<string:stock_number>')
    api.add_resource(StockDaily, '/stock/<string:stock_number>/daily')
    api.add_resource(StockListDaily, '/stock/daily')

    app.run(host="0.0.0.0", debug=True)
