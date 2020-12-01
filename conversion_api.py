from os import error
from flask import Flask, make_response, request
import json
import requests
import pymysql

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
    url = "http://127.0.0.1:3534/speed_request"

    payload={'speed_measure1': speed_measure1,
    'speed_measure2': speed_measure2,
    'speed_value': speed_value}

    headers = {"Content-Type": "application/json",  
    'Access-Control-Allow-Origin': '*'}

    service_response = requests.request("POST", url, data=payload)

    response = make_response(service_response.json(), service_response.status_code)

    response.headers = headers

    return response


def weight_request(weight_measure1, weight_value, weight_measure2):
    url = "http://127.0.0.1:3534/weight_request"

    payload={'weight_measure1': weight_measure1,
    'weight_measure2': weight_measure2,
    'weight_value': weight_value}

    headers = {"Content-Type": "application/json",  
    'Access-Control-Allow-Origin': '*'}

    service_response = requests.request("POST", url, data=payload)

    response = make_response(service_response.json(), service_response.status_code)

    response.headers = headers

    return response

def temp_request(temp_measure1, temp_value, temp_measure2):
    url = "http://127.0.0.1:3534/temp_request"

    payload={'temp_measure1': temp_measure1,
    'temp_measure2': temp_measure2,
    'temp_value': temp_value}

    headers = {"Content-Type": "application/json",  
    'Access-Control-Allow-Origin': '*'}

    service_response = requests.request("POST", url, data=payload)

    response = make_response(service_response.json(), service_response.status_code)

    response.headers = headers

    return response

@app.route('/conversions', methods=['GET', 'OPTIONS'])
def get_conversions():
    if request.method == 'OPTIONS':
        return cors_response()

    db = pymysql.connect("database-1.cjdljloisiap.us-east-2.rds.amazonaws.com", "clouduser", "cloudsqluser$1", "Conversions")
    cursor = db.cursor()
    cursor.execute('SELECT * From conversions ORDER BY ID DESC LIMIT 5')
    results = cursor.fetchall()
    db.close()

    columns = ['mph', 'kph', 'lbs', 'kg', 'fahrenheit', 'celsius']
    conversions = [{k:v for (k,v) in zip(columns, row[1:]) if v != None} for row in results]

    headers = {"Content-Type": "application/json",  
    'Access-Control-Allow-Origin': '*'}

    response = make_response({'conversions': conversions}, 200)

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
