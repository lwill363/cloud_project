from flask import Flask, make_response, request
import json

app = Flask(__name__)


# app.config["debug"] = True

@app.route('/speed_request', methods=['POST'])
def handle_speed_request():
    speed_measure = request.form.get("speed_measure")
    speed_value = request.form.get("speed_value")
    speedM = speed_measure
    speedV = speed_value

    headers = {"Content-Type": "application/json"}

    response = make_response(

         {'measure': speedM},
         {'value': speedV},
         200
    )


@app.route('/weight_request', methods=['POST'])
def handle_weight_request():
    weight_measure = request.form.get("weight_measure")
    weight_value = request.form.get("weight_value")
    weightM = weight_measure
    weightV = weight_value

    headers = {"Content-Type": "application/json"}

    response = make_response(

         {'measure': weightM},
         {'value': weightV},
         200
    )


@app.route('/temp_request', methods=['POST'])
def handle_temp_request():
    temp_measure = request.form.get("temp_measure")
    temp_value = request.form.get("temp_value")
    tempM = temp_measure
    tempV = temp_value

    headers = {"Content-Type": "application/json"}

    response = make_response(

        {'measure': tempM},
        {'value': tempV},
        200
    )
    response.headers = headers
    return response


app.run(port=3533)
