import json


def display_stacks(stacks):
    data = []
    for stack in stacks:
        tmp = {"id" : stack[0], "name": stack[1], "operation": json.loads(stack[2]), "timestamp" : stack[3]}
        data.append(tmp)
    return data
