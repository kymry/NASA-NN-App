from flask import (Blueprint, Flask, g, url_for, jsonify, request, render_template)
from api.__init__ import mongo

# All views (routes) for the front end -- registered with the app via a blueprint
bp = Blueprint('front_end', __name__, url_prefix='/')  # url_prefix is appended to all URLs in this module


@bp.route('/', methods=['GET'])
def home():

    # pulls in one random JSON document from the database
    json_obj = mongo.db.movie.find_one()

    # invokes the Jinja2 template engine
    return render_template('index.html', title='Home', json_display=json_obj["name"])


@bp.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
