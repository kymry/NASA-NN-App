from flask import Flask, jsonify, request, render_template
import sqlite3
import numpy as np
import pickle
import os
import json
from flask_pymongo import PyMongo  # uses MongoDb's Python client API internally

''' This can be seen as the model, view and controller in an MVC framework (if only conceptually)
    Model: the database connections and associated CRUD operations
    View: is jinja3 templating engine which generates the HTML pages from the templates
    Controller: initialization (of Flask), routing of the URLs, and execution (of db and the app)
 '''

# creates the Flask application object
app = Flask(__name__)
app.config.from_object('config')
mongo = PyMongo(app)  # Flask object is sent as parameter to PyMango
#model = pickle.load(open('TODO.pickle', 'rb'))


@app.route('/', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def home():

    # pulls in one random document from MongoDB
    json_obj = mongo.db.movie.find_one()

    # invokes the Jinja2 template engine
    return render_template('index.html', title='Home', json_display=json_obj["name"])

'''
@app.route('/api', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    # convert the JSON to a 2D numpy array and use as parameter in predict function
    prediction = model.predict([[np.array(data['exp'])]])
    output = prediction[0]
    return jsonify(output)
'''


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == '__main__':
    app.run(port=5000, debug=True)
