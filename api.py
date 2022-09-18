from flask import Flask, Blueprint, render_template, redirect, url_for, request, jsonify
from flask_cors import CORS, cross_origin
import sqlite3 as db
import json


from database_operations.db import DB_Service as db
from operate.op import OP_Service as OP_Service

from flask_swagger_ui import get_swaggerui_blueprint

from tools import *

app = Flask(__name__)
CORS(app, support_credentials=True)

api = Blueprint('api', __name__)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "RPN_api"
    }
)
api.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

# Get data from the request if it's a form or a json
def api_get_data(request):
    if request.method == 'POST':
        if len(request.form) > 0:
            return request.form
        else:
            try:
                return request.json
            except Exception as e:
                print(e)
                return request
    else:
        return []

#Default endpoint
@api.route("/", methods=['GET',])
@cross_origin(supports_credentials=True)
def hello_world():

    return "<p>Hello RPN!</p>"


#Create a new operation stack
@api.route("/rpm/create_stack", methods=['POST',])
@cross_origin(supports_credentials=True)
def create_stack():
    #get payload
    rq_data = api_get_data(request)

    #prepare the data
    operation = rq_data.get('operation').split()
    name = rq_data.get('name')
    data =  (name, json.dumps(operation))

    #Create a new stack with the data
    stack_id = db().create_new_stack(data)

    #Prepare the response
    stack = db().get_stack(stack_id)
    pretty_stack = display_stacks(stack)

    return jsonify(pretty_stack), 200


#List all the stacks in the database
@api.route("/rpm/list_stacks", methods=['GET',])
@cross_origin(supports_credentials=True)
def list_stacks():

    stacks = db().list_stacks()
    pretty_stack = display_stacks(stacks)
    return jsonify(pretty_stack), 200


#Get a specific stack
@api.route("/rpm/get_stack/<stack_id>", methods=['GET',])
@cross_origin(supports_credentials=True)
def get_stack(stack_id):

    stack = db().get_stack(stack_id)
    if len(stack) == 0:
        return jsonify('ID not found'), 404
    pretty_stack = display_stacks(stack)
    return jsonify(pretty_stack), 200


# Add new operands to the stack
@api.route("/rpm/add_to_stack/<stack_id>", methods=['POST',])
@cross_origin(supports_credentials=True)
def add_to_stack(stack_id):
    #Get the payload
    data = api_get_data(request)

    # Setup the data
    new_value = data.get('value').split()

    #Find the stack the user is looking for
    stack = db().get_stack(stack_id)
    if len(stack) == 0:
        return jsonify('ID not found'), 404

    # Add the new value on the stack
    op = json.loads(stack[0][2])
    op += new_value
    task = (json.dumps(op), stack_id)

    # Update the stack with the new value in db
    db().insert_new_value(task)

    #Prepare the response
    stack = db().get_stack(stack_id)
    pretty_stack = display_stacks(stack)
    return jsonify(pretty_stack), 200


# Execute one or more operations on the stack
@api.route("/rpm/execute_operation/<stack_id>", methods=['POST',])
@cross_origin(supports_credentials=True)
def execute_operation(stack_id):
    #Get the payload
    data = api_get_data(request)

    #Prepare the data
    operations = data.get('value').split()

    #Get the stack the user is looking for
    stack = db().get_stack(stack_id)
    if len(stack) == 0:
        return jsonify('ID not found'), 404
    op_stack = json.loads(stack[0][2])
    if len(op_stack) < 2:
        return jsonify('Not enough operands'), 400

    # Check what operation the user wants to perform and perform it
    for op in operations:
        #Get the last two element of the stack
        elements = op_stack[-2:]
        result = 0
        if op == "+":
            op_stack = OP_Service().add_(elements, op_stack)

        elif op == "-":
            op_stack = OP_Service().sub_(elements, op_stack)

        elif op == "*":
            op_stack = OP_Service().mul_(elements, op_stack)

        elif op == "/":
            op_stack = OP_Service().full_div_(elements, op_stack)

        elif op == "//":
            op_stack = OP_Service().div_(elements, op_stack)

        elif op == "%":
            op_stack = OP_Service().mod_(elements, op_stack)

        else:
            return jsonify('Operator not suported'), 400

    #Update the stack
    task = (json.dumps(op_stack), stack_id)

    #Insert the updated stack in database
    db().insert_new_value(task)

    #Prepare the response
    stack = db().get_stack(stack_id)
    pretty_stack = display_stacks(stack)
    return jsonify(pretty_stack), 200


#Delete a stack
@api.route("/rpm/delete_stack/<stack_id>", methods=['DELETE',])
@cross_origin(supports_credentials=True)
def delete_stack(stack_id):

    stack = db().get_stack(stack_id)
    if len(stack) == 0:
        return jsonify('ID not found'), 404
    db().delete_stack(stack_id)

    return jsonify("Stack was deleted"), 200


#Update a stack name
@api.route("/rpm/update_stack_name/<stack_id>", methods=['POST',])
@cross_origin(supports_credentials=True)
def update_stack_name(stack_id):
    #Get payload
    data = api_get_data(request)
    new_value = data.get('value')

    #Find the stack the user is looking for
    stack = db().get_stack(stack_id)
    if len(stack) == 0:
        return jsonify('ID not found'), 404

    #Update the stack's name in db
    task = (new_value, stack_id)
    db().update_stack_name(task)

    #Prepare the response
    stack = db().get_stack(stack_id)
    pretty_stack = display_stacks(stack)
    return jsonify(pretty_stack), 200
