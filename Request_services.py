from flask import Flask, make_response, request
import pymysql
import json

app = Flask(__name__)
# format should be pymysql.connect("localhost", "user", "password", "dbname")
db = pymysql.connect("localhost", "user", "password", "dbname")
cursor = db.cursor()
# app.config["debug"] = True

@app.route('/speed_request', methods=['POST'])
def handle_speed_request():
    speed_measure1 = request.form.get("speed_measure1")
    speed_measure2 = request.form.get("speed_measure2")
    speed_value = request.form.get("speed_value")

    headers = {"Content-Type": "application/json"}

    if speed_measure1 == 'mph' and speed_measure2 == 'kph':
        result = speed_value * 1.609344
        query = "INSERT into conversions(Mph, kph) values (%s, %s)"
        cursor.execute(query, (speed_value, result))
        db.commit()
        response = make_response(
            {'kph': result},
            200
        )
        response.headers = headers
        db.close()
        return response
    elif speed_measure1 == 'kph' and speed_measure2 == 'mph':
        result = speed_value / 1.609344
        query = "INSERT into conversions(Kph, Mph) values (%s, %s)"
        cursor.execute(query, (speed_value, result))
        db.commit()
        response = make_response(
            {'mph': result},
            200
        )
        response.headers = headers
        db.close()
        return response
    else:
        response = make_response(
            {'error': 'Invalid speed request format'},
            400
        )
        response.headers = headers
        db.close()
        return response


@app.route('/weight_request', methods=['POST'])
def handle_weight_request():
    weight_measure1 = request.form.get("weight_measure1")
    weight_measure2 = request.form.get("weight_measure2")
    weight_value = request.form.get("weight_value")

    headers = {"Content-Type": "application/json"}

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
        db.close()
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
        db.close()
        return response
    else:
        response = make_response(
            {'error': 'Invalid weight request format'},
            400
        )
        response.headers = headers
        db.close()
        return response



@app.route('/temp_request', methods=['POST'])
def handle_temp_request():
    temp_measure1 = request.form.get("temp_measure1")
    temp_measure2 = request.form.get("temp_measure2")
    temp_value = request.form.get("temp_value")

    headers = {"Content-Type": "application/json"}

    if temp_measure1 == 'fahren' and temp_measure2 == 'cels':
        result = (temp_value - 32) * (5 / 9)
        query = "INSERT into conversions(Fahrenheit, Celsius) values (%s, %s)"
        cursor.execute(query, (temp_value, result))
        db.commit()
        response = make_response(
            {'cels': result},
            200
        )
        response.headers = headers
        db.close()
        return response

    elif temp_measure1 == 'cels' and temp_measure2 == 'fahren':
        result = (temp_value * (9 / 5)) + 32
        query = "INSERT into conversions(Celsius, Fahrenheit) values (%s, %s)"
        cursor.execute(query, (temp_value, result))
        db.commit()
        response = make_response(
            {'fahren': result},
            200
        )
        response.headers = headers
        db.close()
        return response
    else:
        response = make_response(
            {'error': 'Invalid temp request format'},
            400
        )
        response.headers = headers
        db.close()
        return response


app.run(port=3534)
