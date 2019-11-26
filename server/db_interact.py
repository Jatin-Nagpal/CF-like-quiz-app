from server.db import get_db

def roll_number_taken(roll_number):
	db = get_db()
	return db.execute("SELECT id FROM students WHERE roll_number = ?", (roll_number, )).fetchone() is not None
	
	
def email_id_taken(email_id):
	db = get_db()
	return db.execute("SELECT id FROM admins WHERE email_id = ?", (email_id, )).fetchone() is not None
	
	
def add_student(name, roll_number, phone_number, password):
	db = get_db()
	db.execute("INSERT INTO students(name, roll_number, phone_number, password) VALUES(?, ?, ?, ?)", (name, roll_number, phone_number, password))
	db.commit()
	
	
def add_admin(name, email_id, password):
	db = get_db()
	db.execute("INSERT INTO admins(name, email_id, password) VALUES(?, ?, ?)", (name, email_id, password))
	db.commit()


def get_student(roll_number):
	db = get_db()
	user = db.execute("SELECT * FROM students WHERE roll_number = ?", (roll_number, )).fetchone()
	return user
	
	
def get_admin(email_id):
	db = get_db()
	user = db.execute("SELECT * FROM admins WHERE email_id = ?", (email_id, )).fetchone()
	return user


def add_test(name, start_time, duration):
	db = get_db()
	db.execute("INSERT INTO tests(name, start_time, duration) VALUES(?, ?, ?)", (name, start_time, duration))
	db.commit()
	
	
def get_all_tests():
	db = get_db()
	all_tests = db.execute("SELECT * FROM tests")
	return all_tests


def get_test(test_id):
	db = get_db()
	test = db.execute("SELECT * FROM tests WHERE id = ?", (test_id, )).fetchone()
	return test


def update_test(test_id, name, start_time, duration):
	db = get_db()
	db.execute("UPDATE tests SET name = ?, start_time = ?, duration = ? WHERE id = ?", (name, start_time, duration, test_id))
	db.commit()


def get_question(test_id, question_id):
	db = get_db()
	question = db.execute("SELECT * FROM questions WHERE test_id = ? AND question_id = ?", (test_id, question_id)).fetchone()
	return question
	
	
def add_question(test_id, question_id, statement, option_a, option_b, option_c, option_d, correct_option):
	db = get_db()
	db.execute("INSERT INTO questions(test_id, question_id, statement, option_a, option_b, option_c, option_d, correct_option) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (test_id, question_id, statement, option_a, option_b, option_c, option_d, correct_option))
	db.commit()


def update_question(test_id, question_id, statement, option_a, option_b, option_c, option_d, correct_option):
	db = get_db()
	db.execute("UPDATE questions SET statement = ?, option_a = ?, option_b = ?, option_c = ?, option_d = ?, correct_option = ? WHERE test_id = ? AND question_id = ?", (statement, option_a, option_b, option_c, option_d, correct_option, test_id, question_id))
	db.commit()

	
def update_questions_count(test_id, prv_count):
	db = get_db()
	db.execute("UPDATE tests SET questions_count = ? WHERE id = ?", (prv_count + 1, test_id))
	db.commit()


def get_questions(test_id):
	db = get_db()
	questions = db.execute("SELECT * FROM questions WHERE test_id = ?", (test_id, ))
	return questions
	
	
def add_response(test_id, question_id, student_id, marked_option):
	db = get_db()
	db.execute("INSERT INTO responses(test_id, question_id, student_id, marked_option) VALUES(?, ?, ?, ?)", (test_id, question_id, student_id, marked_option))
	db.commit()
	
	
def add_score(test_id, student_id, score):
	db = get_db()
	db.execute("INSERT INTO results(test_id, student_id, score) VALUES (?, ?, ?)", (test_id, student_id, score))
	db.commit()
  

def get_results(test_id):
	db = get_db()
	results = db.execute("SELECT * FROM results JOIN students ON results.student_id = students.id WHERE test_id = ? ORDER BY score DESC ", (test_id, )).fetchall()
	return results
