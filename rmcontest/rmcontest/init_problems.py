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

"""

def get_filename(filepath):
	return os.path.splitext(os.path.basename(filepath))[0]


problem_points = {
	0:0,
	1:1,
	2:1,
	3:2,
	4:2,
	5:3,
	6:4,
	7:5
}


solutions_dir = os.path.join(os.environ['RMCONTEST_ROOT'],'problems','solutions')
input_dir = os.path.join(os.environ['RMCONTEST_ROOT'],'problems','input')
sys.path.insert(0, solutions_dir)

solution_modules = list(
	map(
		get_filename,
		filter(
			lambda x: x.startswith('solution') and x.endswith('.py'),
			os.listdir(solutions_dir)
			)
		)
	)

conn = sqlite3.connect("rmcontest.db")
cur = conn.execute('drop table if exists problems')
cur = conn.execute(
	"""
	create table problems (
	    problem_num INTEGER PRIMARY KEY,
	    problem_answer TEXT NOT NULL,
	    problem_points INTEGER  
	);
	"""
)

for solution_module in solution_modules:
	problem_num = int(solution_module[solution_module.index('_') + 1:])
	mod = importlib.import_module(solution_module)

	input_filepath = os.path.join(input_dir,'input_' + str(problem_num) + '.txt')
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


