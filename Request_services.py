from flask import Flask, make_response, request
import pymysql
import json

app = Flask(__name__)
# format should be pymysql.connect("localhost", "user", "password", "dbname")
db = pymysql.connect("database-1.cjdljloisiap.us-east-2.rds.amazonaws.com", "clouduser", "cloudsqluser$1", "Conversions")
cursor = db.cursor()
# app.config["debug"] = True

def cors_response():
    headers = {'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': '*'}
    response = make_response()
    response.headers = headers
    return response

@app.route('/speed_request', methods=['POST', 'OPTIONS'])
def handle_speed_request():
    if request.method == 'OPTIONS':
        return cors_response()

    headers = {"Content-Type": "application/json",  
            'Access-Control-Allow-Origin': '*'}

    speed_measure1 = request.form.get("speed_measure1")
    speed_measure2 = request.form.get("speed_measure2")
    speed_value = request.form.get("speed_value")
    try:
        speed_value = float(speed_value)
    except:
        response = make_response(
        {'error': 'form field \'speed_value\' could not be converted to a float'},
        400
        )
        response.headers = headers
        return response

    if speed_measure1 == 'mph' and speed_measure2 == 'kph':
        result = speed_value * 1.609344
        query = "INSERT into conversions(mph, kph) values (%s, %s)"
        cursor.execute(query, (speed_value, result))
        db.commit()
        response = make_response(
            {'kph': result},
            200
        )
        response.headers = headers
        
        return response
    elif speed_measure1 == 'kph' and speed_measure2 == 'mph':
        result = speed_value / 1.609344
        query = "INSERT into conversions(kph, mph) values (%s, %s)"
        cursor.execute(query, (speed_value, result))
        db.commit()
        response = make_response(
            {'mph': result},
            200
        )
        response.headers = headers
        
        return response
    else:
        response = make_response(
            {'error': 'Invalid speed request format'},
            400
        )
        response.headers = headers
        
        return response


@app.route('/weight_request', methods=['POST', 'OPTIONS'])
def handle_weight_request():
    if request.method == 'OPTIONS':
        return cors_response()

    headers = {"Content-Type": "application/json",  
            'Access-Control-Allow-Origin': '*'}

    weight_measure1 = request.form.get("weight_measure1")
    weight_measure2 = request.form.get("weight_measure2")
    weight_value = request.form.get("weight_value")
    try:
        weight_value = float(weight_value)
    except:
        response = make_response(
        {'error': 'form field \'weight_value\' could not be converted to a float'},
        400
        )
        response.headers = headers
        return response


    if weight_measure1 == 'lbs' and weight_measure2 == 'kg':
        result = weight_value * 0.45359237
        query = "INSERT into conversions(lbs, kg) values (%s, %s)"
        cursor.execute(query, (weight_value, result))
        db.commit()
        response = make_response(
            {'kg': result},
            200
        )
        response.headers = headers
        
        return response

    elif weight_measure1 == 'kg' and weight_measure2 == 'lbs':
        result = weight_value / 0.45359237
        query = "INSERT into conversions(kg, lbs) values (%s, %s)"
        cursor.execute(query, (weight_value, result))
        db.commit()
        response = make_response(
            {'lbs': result},
            200
        )
        response.headers = headers
        
        return response
    else:
        response = make_response(
            {'error': 'Invalid weight request format'},
            400
        )
        response.headers = headers
        
        return response



@app.route('/temp_request', methods=['POST', 'OPTIONS'])
def handle_temp_request():
    if request.method == 'OPTIONS':
        return cors_response()

    headers = {"Content-Type": "application/json",  
            'Access-Control-Allow-Origin': '*'}

    temp_measure1 = request.form.get("temp_measure1")
    temp_measure2 = request.form.get("temp_measure2")
    temp_value = request.form.get("temp_value")
    try:
        temp_value = float(temp_value)
    except:
        response = make_response(
        {'error': 'form field \'temp_value\' could not be converted to a float'},
        400
        )
        response.headers = headers
        return response


    if temp_measure1 == 'fahrenheit' and temp_measure2 == 'celsius':
        result = (temp_value - 32) * (5 / 9)
        query = "INSERT into conversions(fahrenheit, celsius) values (%s, %s)"
        cursor.execute(query, (temp_value, result))
        db.commit()
        response = make_response(
            {'celsius': result},
            200
        )
        response.headers = headers
        
        return response

    elif temp_measure1 == 'celsius' and temp_measure2 == 'fahrenheit':
        result = (temp_value * (9 / 5)) + 32
        query = "INSERT into conversions(celsius, fahrenheit) values (%s, %s)"
        cursor.execute(query, (temp_value, result))
        db.commit()
        response = make_response(
            {'fahrenheit': result},
            200
        )
        response.headers = headers
        
        return response
    else:
        response = make_response(
            {'error': 'Invalid temp request format'},
            400
        )
        response.headers = headers
        
        return response


app.run(port=3534)
