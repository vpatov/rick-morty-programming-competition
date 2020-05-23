drop table if exists problems;
create table problems (
    problem_num INTEGER PRIMARY KEY,
    problem_answer TEXT NOT NULL,
    problem_points INTEGER  
);

drop table if exists users;
create table users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  hashed_password TEXT NOT NULL,
  time_last_attempt REAL,
  points INTEGER NOT NULL
);

drop table if exists progress;
create table progress (
    problem_num INTEGER,
    user_id INTEGER,
    time_finished REAL,
    FOREIGN KEY(problem_num) REFERENCES problems(problem_num),
    FOREIGN KEY(user_id) REFERENCES users(user_id)

);

drop table if exists winners;
create table winners (
    winner_place INTEGER PRIMARY KEY AUTOINCREMENT,
    time_finished REAL,
    user_id INTEGER,
    username TEXT NOT NULL
);

drop table if exists contest_logistics;
create table contest_logistics (
    contest_started INTEGER NOT NULL,
    contest_start_time REAL
);

drop table if exists gist_urls;
create table gist_urls (
  problem_num INTEGER PRIMARY KEY,
  gist_url TEXT NOT NULL
);

