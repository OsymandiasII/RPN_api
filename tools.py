import json

# This file is used to add functions that are usefull but don't belong to a specific part of the program


def display_stacks(stacks):
    data = []
    for stack in stacks:
        tmp = {"id" : stack[0], "name": stack[1], "operation": json.loads(stack[2]), "timestamp" : stack[3]}
        data.append(tmp)
    return data
