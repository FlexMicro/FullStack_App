import mysql.connector
from flask import g

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=g.app.config['DB_HOST'],
            user=g.app.config['DB_USER'],
            password=g.app.config['DB_PASSWORD'],
            database=g.app.config['DB_NAME']
        )
        g.cursor = g.db.cursor(dictionary=True)
    return g.db, g.cursor

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app):
    app.teardown_appcontext(close_db)