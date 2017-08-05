import json
import string
import random
import os
import sys

def gen_password(length):
    return ''.join(random.sample(string.ascii_lowercase,length))

def update_accounts(accounts):
    f = open('accounts','w')
    json.dump(accounts,f)
    f.close()


def init_accounts(usernames):
    accounts = {}
    for username in usernames:
        account = {"password":gen_password(5),"progress":[]}
        accounts[username] = account
    update_accounts(accounts)



def read_accounts():
    f = open('accounts','r')
    accounts = json.load(f)
    f.close()
    return accounts

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    accounts = read_accounts()
    if username in accounts:
        if password == accounts[username]["password"]:
            return (True,0)
        else:
            return (False,"Wrong Password")
    else:
        return (False,"No such username")

def has_completed(username,problem_num):
    accounts = read_accounts()
    return problem_num in accounts[username]["progress"]

def mark_as_completed(username,problem_num):
     accounts = read_accounts()
     accounts[username]["progress"].append(problem_num)
     update_accounts(accounts)



def init_problem_answers():
    problems_dir = 'C:\\Users\\Vasia\\Documents\\projects\\rick_morty_programming_contest\\problems'
    sys.path.insert(0, problems_dir)

    import problem1_solution
    import problem2_solution
    import problem3_solution

    f = open('problem_answers','w')
    problem_answers = {
        1: problem1_solution.get_solution(),
        2: problem2_solution.get_solution(),
        3: problem3_solution.get_solution()
        }
    json.dump(problem_answers,f)
    f.close()

def get_problem_answer(problem_num):
    f = open('problem_answers','r')
    problem_answers = load(f)
    f.close()
    return problem_answers[problem_num]



