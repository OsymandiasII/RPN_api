from flask import Flask


app = Flask(__name__)

from database_operations.db import DB_Service as db

#Operations
#Each op works on the same principle :
#   - Perform the arithmetic operation on the two provided Operands
#   - Remove the last two element of the stack
#   - Add the new result to the end of the operation stack
#   - return the operation stack
class OP_Service:

    # Addition
    def add_(self, elements, op_stack):
        result = float(elements[0]) + float(elements[1])
        op_stack = op_stack[:len(op_stack)-2]
        op_stack.append(str(result))

        return op_stack

    # Subtraction
    def sub_(self, elements, op_stack):
        result = float(elements[0]) - float(elements[1])
        op_stack = op_stack[:len(op_stack)-2]
        op_stack.append(str(result))

        return op_stack

    # Multiplication
    def mul_(self, elements, op_stack):
        result = float(elements[0]) * float(elements[1])
        op_stack = op_stack[:len(op_stack)-2]
        op_stack.append(str(result))

        return op_stack

    # Full Division
    def full_div_(self, elements, op_stack):
        result = float(elements[0]) / float(elements[1])
        op_stack = op_stack[:len(op_stack)-2]
        op_stack.append(str(result))

        return op_stack

    # Division
    def div_(self, elements, op_stack):
        result = float(elements[0]) // float(elements[1])
        op_stack = op_stack[:len(op_stack)-2]
        op_stack.append(str(result))

        return op_stack

    # Modulo
    def mod_(self, elements, op_stack):
        result = float(elements[0]) % float(elements[1])
        op_stack = op_stack[:len(op_stack)-2]
        op_stack.append(str(result))

        return op_stack
