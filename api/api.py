from flask import Flask, jsonify, request, render_template
import sqlite3, numpy as np, pickle

''' This can be seen as the model, view and controller in an MVC framework (if only conceptually)
    Model: the database connections and associated CRUD operations
    View: is jinja3 templating engine which generates the HTML pages from the templates
    Controller: initialization (of Flask), routing of the URLs, and execution (of db and the app)
 '''

# creates the Flask application object
app = Flask(__name__)
app.config.from_object('config')
#model = pickle.load(open('TODO.pickle', 'rb'))

@app.route('/', methods=['GET'])
def home():
    user = {'username': 'Kymry'}
    # the render_template() function invokes the Jinja2 template engine (will convert to BootStrap instead)
    return render_template('index.html', title='Home', user=user)

'''
@app.route('/api', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    # convert the JSON to a 2D numpy array and use as parameter in predict function
    prediction = model.predict([[np.array(data['exp'])]])
    output = prediction[0]
    return jsonify(output)
'''

# sqllite connection example
'''@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('books.db')
    
    # this object moves through the database to pull the requested data
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM books;').fetchall()

    return jsonify(all_books)'''


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == '__main__':
    app.run(port=5000, debug=True)
