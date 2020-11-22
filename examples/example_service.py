from flask import Flask, make_response, request
import json

app = Flask(__name__)

# Uncomment code below to turn on debugging
# app.config["DEBUG"] = True

@app.route('/example', methods=['GET'])
def handle_getrequest():
    name = request.args.get("name")
    message = ""
    if name == None:
        message = "You have no name"
    else:
        message = "Your name is " + name

    headers = {"Content-Type": "application/json"}
    response = make_response(
    {'message': message},
    200
    )
    response.headers = headers
    return response

@app.route('/example', methods=['POST'])
def handle_postrequest():
    name = request.form.get("name")
    message = ""
    if name == None:
        message = "You have no name"
    else:
        message = "Your name is " + name

    headers = {"Content-Type": "application/json"}
    response = make_response(
    {'message': message},
    200
    )
    response.headers = headers
    return response

app.run(port=3533)
