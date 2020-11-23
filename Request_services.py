from flask import Flask, make_response, request
import json

app = Flask(__name__)


# app.config["debug"] = True

@app.route('/speed_request', methods=['POST'])
def handle_speed_request():
    speed_measure1 = request.form.get("speed_measure1")
    speed_measure2 = request.form.get("speed_measure2")
    speed_value = request.form.get("speed_value")

    headers = {"Content-Type": "application/json"}

    if speed_measure1 == 'mph' and speed_measure2 == 'kph':
        response = make_response(
            {'kph': speed_value * 1.609344},
            200
        )

    elif speed_measure1 == 'kph' and speed_measure2 == 'mph':
        response = make_response(
            {'mph': speed_value / 1.609344},
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


@app.route('/weight_request', methods=['POST'])
def handle_weight_request():
    weight_measure1 = request.form.get("weight_measure1")
    weight_measure2 = request.form.get("weight_measure2")
    weight_value = request.form.get("weight_value")

    headers = {"Content-Type": "application/json"}

    if weight_measure1 == 'lbs' and weight_measure2 == 'kg':
        response = make_response(
            {'kg': weight_value * 0.45359237},
            200
        )

    elif weight_measure1 == 'kg' and weight_measure2 == 'lbs':
        response = make_response(
            {'lbs': weight_value / 0.45359237},
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



@app.route('/temp_request', methods=['POST'])
def handle_temp_request():
    temp_measure1 = request.form.get("temp_measure1")
    temp_measure2 = request.form.get("temp_measure2")
    temp_value = request.form.get("temp_value")

    headers = {"Content-Type": "application/json"}

    if temp_measure1 == 'fahren' and temp_measure2 == 'cels':
        response = make_response(
            {'cels': (temp_value - 32) * (5 / 9)},
            200
        )

    elif temp_measure1 == 'cels' and temp_measure2 == 'fahren':
        response = make_response(
            {'fahren': (temp_value * (9 / 5)) + 32},
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


app.run(port=3533)
