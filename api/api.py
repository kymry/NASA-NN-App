from flask import Flask, jsonify, request, render_template
import sqlite3, numpy as np, pickle

# creates the Flask application object
app = Flask(__name__)
#model = pickle.load(open('TODO.pickle', 'rb'))
app.config["DEBUG"] = True


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
