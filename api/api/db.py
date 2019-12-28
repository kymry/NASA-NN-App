import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

DEFAULT_PATH = '/Users/kymryburwell/Google Drive/Code Repository/NASA ML API/api/databases/marsweather.sqlite3'

# @click register the get_db command with the app instance
@click.command('get_db')
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    ''' Registers all functions with the app instance '''
    app.teardown_appcontext(close_db)
    app.cli.add_command(get_db)


def create_db(connection):
    marsweather_sql = """
    CREATE TABLE sols (
        sol int PRIMARY KEY,
        average_temperature float,
        high_temperature float,
        low_temperature float,
        horizontal_wind_speed float,
        pressure float) """
    connection.execute(marsweather_sql)


