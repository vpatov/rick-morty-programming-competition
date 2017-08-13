import json

f = open('problem5_input.json','r')
tree = json.load(f)

def find_node(target_key,node):
    for key in node:
        if key == target_key:
            return key
        else:
            result = find_node(target_key,node[key])
            if result:
                return key  + result
    return False

code = find_node('LOL',tree)
print(code)
print(code[::4])

def get_solution():
    return code[::4]
