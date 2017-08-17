def get_solution(f=None):
	import json
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
	return code[::4]
