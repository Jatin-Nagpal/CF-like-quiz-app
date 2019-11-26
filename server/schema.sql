DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS admins;
DROP TABLE IF EXISTS tests;
DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS results;
DROP TABLE IF EXISTS test_data;

CREATE TABLE IF NOT EXISTS students (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT,
	roll_number TEXT UNIQUE,
	phone_number TEXT,
	password TEXT
);

CREATE TABLE IF NOT EXISTS admins (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT,
	email_id TEXT UNIQUE,
	password TEXT
);

CREATE TABLE IF NOT EXISTS tests (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT,
	start_time DATETIME,
	duration TIME,
	questions_count INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS questions (
	test_id	INTEGER,
	question_id INTEGER,
	statement TEXT,
	option_a TEXT,
	option_b TEXT,
	option_c TEXT,
	option_d TEXT,
	correct_option TEXT,
	FOREIGN KEY (test_id) REFERENCES "tests"(id)
);

CREATE TABLE IF NOT EXISTS results (
	test_id INTEGER,
	student_id INTEGER,
	score INTEGER,
	FOREIGN KEY (test_id) REFERENCES "tests"(id),
	FOREIGN KEY (student_id) REFERENCES "students"(id)
);

CREATE TABLE IF NOT EXISTS responses (
	test_id INTEGER,
	student_id INTEGER,
	question_id INTEGER,
	marked_option TEXT,
	FOREIGN KEY (test_id) REFERENCES "tests"(id),
	FOREIGN KEY (student_id) REFERENCES "students"(id),
	FOREIGN KEY (question_id) REFERENCES "questions"(id)
);
