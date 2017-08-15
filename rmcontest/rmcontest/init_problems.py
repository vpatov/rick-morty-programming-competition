import sqlite3
import sys
import os
import importlib
"""
drop table if exists problems;
create table problems (
    problem_num INTEGER PRIMARY KEY,
    problem_answer TEXT NOT NULL,
    problem_points INTEGER  
);

Problems
1) Galaxies 1
2) Shleeble number 2
3) zlnop propety search 3
4) sum of numbers 1
5) traverse tree 2 
6) tf-idf 3
7) balanced brackets 1

new order should be

balanced brackets
sum of numbers
galaxies
traverse tree
shleeble number
tf-idf
zlnop

Ordered by difficulty -
4, 1, 5, 2, 3

"""

def get_filename(filepath):
	return os.path.splitext(os.path.basename(filepath))[0]


problem_points = {
	1:1,
	2:1,
	3:1,
	4:2,
	5:2,
	6:3,
	7:3
}


problems_dir = os.path.join(os.getcwd(),'static','problems')
sys.path.insert(0, problems_dir)

solution_modules = list(
	map(
		get_filename,
		filter(
			lambda x: x.startswith('solution') and x.endswith('.py'),
			os.listdir(problems_dir)
			)
		)
	)

conn = sqlite3.connect("rmcontest.db")
for solution_module in solution_modules:
	problem_num = int(solution_module[solution_module.index('_') + 1:])
	mod = importlib.import_module(solution_module)

	input_filepath = os.path.join(problems_dir,'input_' + str(problem_num) + '.txt')
	solution = None
	try:
		input_file = open(input_filepath,'r')
		solution = mod.get_solution(input_file)
	except Exception as e:
		solution = mod.get_solution()

	conn.execute(
		'insert into problems' \
		'(problem_num, problem_answer, problem_points)' \
		'values (%s, "%s", %s);' % \
		(problem_num, solution,problem_points[problem_num])
	)

conn.commit()
conn.close()


