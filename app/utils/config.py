import os
from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import sessionmaker

DB_ENGINE = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(
    os.getenv('DB_USER'),
    os.getenv('DB_PASSWORD'),
    os.getenv('DB_HOST'),
    os.getenv('DB_NAME')
)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_ENGINE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.url_map.strict_slashes = False
api = Api(app)
db = SQLAlchemy(app)
swagger = Swagger(app)

engine = create_engine(DB_ENGINE, encoding='utf-8')
session_factory = sessionmaker(bind=engine, autoflush=False)
Session = scoped_session(session_factory)
