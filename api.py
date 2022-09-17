from flask import Flask, Blueprint, render_template, redirect, url_for, request, jsonify
from flask_cors import CORS, cross_origin
import sqlite3 as db
import json

from doc.doc import auto

from database_operations.db import DB_Service as db
from operate.op import OP_Service as OP_Service

from tools import *

app = Flask(__name__)
CORS(app, support_credentials=True)

api = Blueprint('api', __name__)

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

@api.route("/", methods=['GET',])
@cross_origin(supports_credentials=True)
@auto.doc(groups=['admin'])
def hello_world():

    return "<p>Hello RPN!</p>"

@api.route("/rpm/create_stack", methods=['POST',])
@cross_origin(supports_credentials=True)
@auto.doc(groups=['admin'])
def create_stack():
    rq_data = api_get_data(request)
    operation = rq_data.get('operation').split()
    name = rq_data.get('name')
    data =  (name, json.dumps(operation))
    stack_id = db().create_new_stack(data)
    stack = db().get_stack(stack_id)
    pretty_stack = display_stacks(stack)
    return jsonify(pretty_stack), 200


@api.route("/rpm/list_stacks", methods=['GET',])
@cross_origin(supports_credentials=True)
@auto.doc(groups=['admin'])
def list_stacks():

    stacks = db().list_stacks()
    pretty_stack = display_stacks(stacks)
    return jsonify(pretty_stack), 200


@api.route("/rpm/get_stack/<stack_id>", methods=['GET',])
@cross_origin(supports_credentials=True)
@auto.doc(groups=['admin'])
def get_stack(stack_id):

    stack = db().get_stack(stack_id)
    if len(stack) == 0:
        return jsonify('ID not found'), 404
    pretty_stack = display_stacks(stack)
    return jsonify(pretty_stack), 200



@api.route("/rpm/add_to_stack/<stack_id>", methods=['POST',])
@cross_origin(supports_credentials=True)
@auto.doc(groups=['admin'])
def add_to_stack(stack_id):
    data = api_get_data(request)
    new_value = data.get('value')
    stack = db().get_stack(stack_id)
    if len(stack) == 0:
        return jsonify('ID not found'), 404
    op = json.loads(stack[0][2])
    op.append(new_value)
    task = (json.dumps(op), stack_id)
    db().insert_new_value(task)
    stack = db().get_stack(stack_id)
    pretty_stack = display_stacks(stack)
    return jsonify(pretty_stack), 200


@api.route("/rpm/execute_operation/<stack_id>", methods=['POST',])
@cross_origin(supports_credentials=True)
@auto.doc(groups=['admin'])
def execute_operation(stack_id):
    data = api_get_data(request)
    operations = data.get('value').split()
    stack = db().get_stack(stack_id)
    if len(stack) == 0:
        return jsonify('ID not found'), 404
    op_stack = json.loads(stack[0][2])
    if len(op_stack) < 2:
        return jsonify('Not enough operands'), 400
    for op in operations:
        elements = op_stack[-2:]
        result = 0
        if op == "+":
            op_stack = OP_Service().add_(elements, op_stack)

        elif op == "-":
            op_stack = OP_Service().sub_(elements, op_stack)

        elif op == "*":
            op_stack = OP_Service().mul_(elements, op_stack)

        elif op == "/":
            op_stack = OP_Service().div_(elements, op_stack)

        elif op == "%":
            op_stack = OP_Service().mod_(elements, op_stack)

        else:
            return jsonify('Operator not suported'), 400

    task = (json.dumps(op_stack), stack_id)
    db().insert_new_value(task)
    stack = db().get_stack(stack_id)
    pretty_stack = display_stacks(stack)
    return jsonify(pretty_stack), 200



@api.route("/rpm/delete_stack/<stack_id>", methods=['GET',])
@cross_origin(supports_credentials=True)
@auto.doc(groups=['admin'])
def delete_stack(stack_id):

    stack = db().get_stack(stack_id)
    if len(stack) == 0:
        return jsonify('ID not found'), 404
    db().delete_stack(stack_id)

    return jsonify("Stack was deleted"), 200


@api.route("/rpm/update_stack_name/<stack_id>", methods=['POST',])
@cross_origin(supports_credentials=True)
@auto.doc(groups=['admin'])
def update_stack_name(stack_id):
    data = api_get_data(request)
    new_value = data.get('value')
    stack = db().get_stack(stack_id)
    if len(stack) == 0:
        return jsonify('ID not found'), 404
    task = (new_value, stack_id)
    db().update_stack_name(task)
    stack = db().get_stack(stack_id)
    pretty_stack = display_stacks(stack)
    return jsonify(pretty_stack), 200
