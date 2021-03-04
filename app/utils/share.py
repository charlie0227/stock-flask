from contextlib import contextmanager
from utils.config import Session
import logging

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()

def catch_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log.exception(e)
            return {'message': f'{e}'}, 500 
    return wrapper