'''
@app.route('/api', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    # convert the JSON to a 2D numpy array and use as parameter in predict function
    prediction = model.predict([[np.array(data['exp'])]])
    output = prediction[0]
    return jsonify(output)
'''