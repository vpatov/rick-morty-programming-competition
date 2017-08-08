import json
import string
import random
import os
import time
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
        account = {"password":gen_password(5),"progress":{},"time_last_attempt":0}
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

def get_progress(username):
    accounts = read_accounts()
    return accounts[username]["progress"]

def mark_as_completed(username,problem_num):
    """
    marks the problem as completed, and returns the number of problems left
    for that user to do.
    """
    accounts = read_accounts()
    problems_done = accounts[username]["progress"]
    if problem_num not in problems_done:
        accounts[username]["progress"][problem_num] = time.time()
    update_accounts(accounts)
    return 3 - len(accounts[username]["progress"])

def mark_attempt(username):
    """
    mark that the user attempted the question, such that they cannot attempt 
    too frequently
    """
    accounts = read_accounts()
    last_attempt = accounts[username]["time_last_attempt"]
    current_time = time.time()

    print("Last_attempt: %s" % last_attempt)

    time_left_to_wait = 30 - (current_time - last_attempt)

    if time_left_to_wait >= 1:
        return int(time_left_to_wait) 
    else:
        accounts[username]["time_last_attempt"] = current_time
        update_accounts(accounts)
        return 0



def init_problem_answers():
    problems_dir = os.path.join(os.getcwd(),'static','problems')
    sys.path.insert(0, problems_dir)
    print(sys.path)

    import problem1_solution
    import problem2_solution
    import problem3_solution

    f = open('problem_answers','w')
    problem_answers = {
        1: problem1_solution.get_solution(open(os.path.join(problems_dir,'problem1_input.txt'),'r')),
        2: problem2_solution.get_solution(),
        3: problem3_solution.get_solution(open(os.path.join(problems_dir,'problem3_input.txt'),'r')),
        }
    json.dump(problem_answers,f)
    f.close()

def get_problem_answer(problem_num):
    f = open('problem_answers','r')
    problem_answers = json.load(f)
    f.close()
    return problem_answers[problem_num]

def init_winners():
    winners = []
    f = open('winners','w')
    json.dump(winners,f)
    f.close()



def get_winners():
    f = open('winners','r')
    winners = json.load(f)
    f.close()
    return winners

def add_winner(username,completion_time):
    winners = get_winners()
    winners.append((username,completion_time))
    f = open('winners','w')
    json.dump(winners,f)
    f.close()
    return len(winners)

    



