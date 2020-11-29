from os import error
from flask import Flask, make_response, request
import json

app = Flask(__name__)

# Uncomment code below to turn on debugging
# app.config["DEBUG"] = True

with open('config.json', 'r') as f:
    config = json.load(f)
apikeys = config['api-keys']

def cors_response():
    headers = {'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': '*'}
    response = make_response()
    response.headers = headers
    return response

@app.before_request
def request_authentication():
    if request.method != 'OPTIONS':
        apikey = request.headers.get('x-api-key')
        if apikey == None or apikey not in apikeys:
                headers = {"Content-Type": "application/json",  
                            'Access-Control-Allow-Origin': '*'}
                response = make_response(
                    {'error': 'missing or invalid api key'},
                    401
                )
                response.headers = headers
                return response

@app.route('/<service_type>/<service_measure1>/<float:measure1_value>/<service_measure2>', methods=['GET', 'OPTIONS'])
@app.route('/<service_type>/<service_measure1>/<int:measure1_value>/<service_measure2>', methods=['GET', 'OPTIONS'])
def handle_request(service_type, service_measure1, measure1_value, service_measure2):
    if request.method == 'OPTIONS':
        return cors_response()
    elif service_type == 'speed':
        return speed_request(service_measure1, measure1_value, service_measure2)
    elif service_type == 'weight':
        return weight_request(service_measure1, measure1_value, service_measure2)
    elif service_type == 'temperature':
        return temp_request(service_measure1, measure1_value, service_measure2)
    else:
        return invalid_servicetype()

@app.route('/convert', methods=['POST', 'OPTIONS'])
def handle_postrequest():
    if request.method == 'OPTIONS':
        return cors_response()
    service_type = request.form.get('service_type')
    service_measure1 = request.form.get('from_measurement')
    service_measure2 = request.form.get('to_measurement')
    measure1_value = request.form.get('measurement_value')
    error_message = ""
   
    if service_type == None:
       error_message = 'missing form field \'service_type\''
    elif service_measure1 == None:
        error_message = 'missing form field \'from_measurement\''
    elif service_measure2 == None:
        error_message = 'missing form field \'to_measurement\''
    elif measure1_value == None:
        error_message = 'missing form field \'measurement_value\''

    if error_message != "":
        headers = {"Content-Type": "application/json",  
            'Access-Control-Allow-Origin': '*'}
        response = make_response(
        {'error': error_message},
        400
        )
        response.headers = headers
        return response
    else:
        try:
            measure1_value = float(measure1_value)
            return handle_request(service_type, service_measure1, measure1_value, service_measure2)
        except:
            headers = {"Content-Type": "application/json",  
            'Access-Control-Allow-Origin': '*'}
            response = make_response(
            {'error': 'form field \'measurement_value\' could not be converted to a float'},
            400
            )
            response.headers = headers
            return response

def speed_request(speed_measure1, speed_value, speed_measure2):
    headers = {"Content-Type": "application/json",  
            'Access-Control-Allow-Origin': '*'}
    if speed_measure1 == 'mph' and speed_measure2 == 'kph':
        response = make_response(
        {'kph': speed_value * 1.609344},
        200
        )
        response.headers = headers
        return response
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

def weight_request(weight_measure1, weight_value, weight_measure2):
    headers = {"Content-Type": "application/json",  
            'Access-Control-Allow-Origin': '*'}
    if weight_measure1 == 'lbs' and weight_measure2 == 'kg':
        response = make_response(
        {'kg': weight_value * 0.45359237},
        200
        )
        response.headers = headers
        return response
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

def temp_request(temp_measure1, temp_value, temp_measure2):
    headers = {"Content-Type": "application/json",  
            'Access-Control-Allow-Origin': '*'}
    if temp_measure1 == 'fahrenheit' and temp_measure2 == 'celsius':
        response = make_response(
        {'celsius': (temp_value - 32) * (5/9)},
        200
        )
        response.headers = headers
        return response
    elif temp_measure1 == 'celsius' and temp_measure2 == 'fahrenheit':
        response = make_response(
        {'fahrenheit': (temp_value * (9 / 5)) + 32},
        200
        )
        response.headers = headers
        return response
    else:
        response = make_response(
        {'error': 'Invalid temperature request format'},
        400
        )
        response.headers = headers
        return response

def invalid_servicetype():
    headers = {"Content-Type": "application/json",  
            'Access-Control-Allow-Origin': '*'}
    response = make_response(
    {'error': 'Invalid service type'},
    400
    )
    response.headers = headers
    return response

@app.errorhandler(404)
def page_not_found(error):
    headers = {"Content-Type": "application/json",  
                'Access-Control-Allow-Origin': '*'}
    response = make_response(
        {'error': 'invalid request'},
        404
    )
    response.headers = headers
    return response

@app.errorhandler(400)
def bad_request(error):
    headers = {"Content-Type": "application/json",  
            'Access-Control-Allow-Origin': '*'}
    response = make_response(
        {'error': 'bad request'},
        400
    )
    response.headers = headers
    return response

@app.errorhandler(500)
def server_error(error):
    headers = {"Content-Type": "application/json",  
            'Access-Control-Allow-Origin': '*'}
    response = make_response(
        {'error': 'server error'},
        500
    )
    response.headers = headers
    return response

app.run(port=3533)
