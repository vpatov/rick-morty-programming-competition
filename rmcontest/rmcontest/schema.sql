drop table if exists problems;
create table problems (
    problem_id INTEGER PRIMARY KEY AUTOINCREMENT,
    problem_text TEXT NOT NULL,
    problem_answer INTEGER NOT NULL  
);

drop table if exists users;
create table users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  password TEXT NOT NULL,
  time_last_attempt TIMESTAMP
);

drop table if exists progress;
create table progress (
    problem_id INTEGER,
    user_id INTEGER,
    time_finished TIMESTAMP,
    FOREIGN KEY(problem_id) REFERENCES problems(problem_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    CONSTRAINT progress_key PRIMARY KEY (problem_id, user_id)

);

-- progress_id INTEGER PRIMARY KEY AUTOINCREMENT,