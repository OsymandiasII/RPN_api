from flask import Flask


app = Flask(__name__)

from database_operations.db import DB_Service as db


class OP_Service:

    def add_(self, elements, op_stack):
        result = float(elements[0]) + float(elements[1])
        op_stack = op_stack[:len(op_stack)-2]
        op_stack.append(str(result))

        return op_stack

    def sub_(self, elements, op_stack):
        result = float(elements[0]) - float(elements[1])
        op_stack = op_stack[:len(op_stack)-2]
        op_stack.append(str(result))

        return op_stack

    def mul_(self, elements, op_stack):
        result = float(elements[0]) * float(elements[1])
        op_stack = op_stack[:len(op_stack)-2]
        op_stack.append(str(result))

        return op_stack

    def div_(self, elements, op_stack):
        result = float(elements[0]) / float(elements[1])
        op_stack = op_stack[:len(op_stack)-2]
        op_stack.append(str(result))

        return op_stack


    def mod_(self, elements, op_stack):
        result = float(elements[0]) % float(elements[1])
        op_stack = op_stack[:len(op_stack)-2]
        op_stack.append(str(result))

        return op_stack
