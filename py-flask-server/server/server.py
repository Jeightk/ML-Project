from flask import Flask, request, jsonify
import util
app = Flask(__name__)

@app.route('/get_location_names')
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    
    total_sqft = float(request.form['TotalSqft'])
    location = request.form['Location']
    bed = int(request.form['Bedroom'])
    bath = int(request.form['Bathroom'])

    response =  jsonify({
        #'hi': 'hi'
        'estimated_price': util.get_estimated_price(location, total_sqft, bed, bath)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

if __name__ == "__main__":
    print("Starting python flask server")
    app.run()