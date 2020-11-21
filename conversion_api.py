from flask import Flask, make_response, request
import json

app = Flask(__name__)

# Uncomment code for below to turn on debugging
# app.config["DEBUG"] = True

with open('config.json', 'r') as f:
    config = json.load(f)
apikeys = config['api-keys']

@app.before_request
def request_authentication():
    apikey = request.headers.get('x-api-key')
    if apikey == None or apikey not in apikeys:
            headers = {"Content-Type": "application/json"}
            response = make_response(
                {'error': 'missing or invalid api key'},
                401
            )
            response.headers = headers;
            return response;

@app.route('/<service_type>/<service_measure1>/<float:measure1_value>/<service_measure2>', methods=['GET'])
@app.route('/<service_type>/<service_measure1>/<int:measure1_value>/<service_measure2>', methods=['GET'])
def handle_request(service_type, service_measure1, measure1_value, service_measure2):
    if service_type == 'speed':
        return speed_request(service_measure1, measure1_value, service_measure2)
    elif service_type == 'weight':
        return weight_request(service_measure1, measure1_value, service_measure2)
    elif service_type == 'temperature':
        return temp_request(service_measure1, measure1_value, service_measure2)
    else:
        return invalid_servicetype()

def speed_request(speed_measure1, speed_value, speed_measure2):
    headers = {"Content-Type": "application/json"}
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
    headers = {"Content-Type": "application/json"}
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
    headers = {"Content-Type": "application/json"}
    if temp_measure1 == 'fahren' and temp_measure2 == 'cels':
        response = make_response(
        {'celsius': (temp_value - 32) * (5/9)},
        200
        )
        response.headers = headers
        return response
    elif temp_measure1 == 'cels' and temp_measure2 == 'fahren':
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
    headers = {"Content-Type": "application/json"}
    response = make_response(
    {'error': 'Invalid service type'},
    400
    )
    response.headers = headers
    return response

@app.errorhandler(404)
def page_not_found(error):
    headers = {"Content-Type": "application/json"}
    response = make_response(
        {'error': 'invalid request'},
        404
    )
    response.headers = headers;
    return response;

@app.errorhandler(400)
def bad_request(error):
    headers = {"Content-Type": "application/json"}
    response = make_response(
        {'error': 'bad request'},
        400
    )
    response.headers = headers;
    return response;

@app.errorhandler(500)
def server_error(error):
    headers = {"Content-Type": "application/json"}
    response = make_response(
        {'error': 'server error'},
        500
    )
    response.headers = headers;
    return response;

app.run(port=3533)