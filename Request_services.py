from flask import Flask, make_response, request
import json

app = Flask(__name__)


# app.config["debug"] = True

@app.route('/speed_request', methods=['POST'])
def handle_speed_request():
    speed_measure = request.form.get("speed_measure")
    speed_value = request.form.get("speed_value")
    values = speed_measure + speed_value

    headers = {"Content-Type": "application/json"}

    response = make_response(

        {'values': values},
        200
    )
    response.headers = headers
    return response


@app.route('/weight_request', methods=['POST'])
def handle_weight_request():
    weight_measure = request.form.get("weight_measure")
    weight_value = request.form.get("weight_value")
    values = weight_measure + weight_value

    headers = {"Content-Type": "application/json"}

    response = make_response(

        {'values': values},
        200
    )
    response.headers = headers
    return response


@app.route('/temp_request', methods=['POST'])
def handle_temp_request():
    temp_measure = request.form.get("temp_measure")
    temp_value = request.form.get("temp_value")
    values = temp_measure + temp_value

    headers = {"Content-Type": "application/json"}

    response = make_response(

        {'values': values},
        200
    )
    response.headers = headers
    return response


app.run(port=3533)
