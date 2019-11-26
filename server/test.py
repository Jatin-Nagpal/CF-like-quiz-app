from flask import Blueprint, render_template, request, redirect, url_for, session
from server.db_interact import *
from server.auth import login_admin_required, login_student_required, logged_in_required
import re

bp = Blueprint("test", __name__)

@bp.route("/create_test/", methods = ("GET", "POST"))
@login_admin_required
def create_test():
	if request.method == "POST":
		name = request.form["name"]
		start_time = request.form["start_time"]
		duration = request.form["duration"]
		add_test(name, start_time, duration)
		print("Test {} added.".format(name))
		return redirect(url_for("test.tests"))
	else:
		return render_template("test/create_test.html")
		

@bp.route("/tests/")
@logged_in_required
def tests():
	tests_table = get_all_tests()
	all_tests = []
	for test in tests_table:
		to_add = {
			"id": test["id"],
			"name": test["name"],
			"start_time": test["start_time"],
			"duration": test["duration"]
		}
		prv = re.split("-|T|:", to_add["start_time"])
		to_add["start_day"] = str(prv[2]) + "/" + str(prv[1]) + "/" + str(prv[0])
		to_add["start_time"] = str(prv[3]) + ":" + str(prv[4])
		all_tests += [to_add]
	return render_template("test/tests.html", all_tests = all_tests)
	
	
@bp.route("/edit_test/<int:test_id>/", methods = ("GET", "POST"))
@login_admin_required
def edit_test(test_id):
	test = get_test(test_id)
	if test is None:
		print("Invalid test: {}".format(test_id))
		return redirect(url_for("test.tests"))
	if request.method == "POST":
		name = request.form["name"]
		start_time = request.form["start_time"]
		duration = request.form["duration"]
		update_test(test_id, name, start_time, duration)
		print("Test {} updated.".format(name))
		return redirect(url_for("test.edit_test", test_id = test_id))
	else:
		return render_template("test/edit_test.html", test = test)
		

@bp.route("/test/<int:test_id>/question/<int:question_id>/", methods = ("GET", "POST"))
@login_admin_required
def test(test_id, question_id):
	test = get_test(test_id)
	if test is None:
		print("Invalid test: {}".format(test_id))
		return redirect(url_for(test.tests))
	question = get_question(test_id, question_id)
	if question is None:
		print("Invalid question: {} of test: {}".format(question_id, test_id))
		return redirect(url_for("test.tests"))
	is_new_question = (question_id == test["questions_count"] + 1)
	print(is_new_question)
	if request.method == "POST":
		statement = request.form["statement"]
		option_a = request.form["option_a"]
		option_b = request.form["option_b"]
		option_c = request.form["option_c"]
		option_d = request.form["option_d"]
		correct_option = request.form["correct_option"]
		print("Correct option is: {}".format(correct_option))
		if is_new_question:
			add_question(test_id, question_id, statement, option_a, option_b, option_c, option_d, correct_option)
			update_questions_count(test_id, test["questions_count"])
			print("Added question {} to test {}".format(question_id, test_id))
		else:
			update_question(test_id, question_id, statement, option_a, option_b, option_c, option_d, correct_option)
			print("Updated question {} of test {}".format(question_id, test_id))
		return redirect(url_for("test.test", test_id = test_id, question_id = question_id))
	else:
		return render_template("test/test.html", test = test, question = question, question_id = question_id)
    

@bp.route("/test/<int:test_id>/", methods = ("GET", "POST"))
@login_student_required
def test_student(test_id):
	test = get_test(test_id)
	if test is None:
		print("Invalid test: {}".format(test_id))
		return redirect(url_for("test.tests"))
	questions = get_questions(test_id)
	if request.method == "POST":
		score = 0
		for question_id in range(1, test["questions_count"] + 1):
			if str(question_id) in request.form:
				marked_option = request.form[str(question_id)]
				add_response(test_id, question_id, session["student_id"], marked_option)
				question = get_question(test_id, question_id)
				if question["correct_option"] == marked_option:
					score += 1
		add_score(test_id, session["student_id"], score)
		return redirect(url_for("test.tests"))
	else:
		return render_template("test/test_student.html", questions = questions, test = test)
    

@bp.route("/standings/<int:test_id>/")
@logged_in_required
def standings(test_id):
	test = get_test(test_id)
	if test is None:
		return redirect(url_for("test.tests"))
	result_table = get_results(test_id)
	counter, max_score = 1, -1
	results = []
	for student in result_table:
		to_add = {
			"roll_number": student["roll_number"],
			"name": student["name"],
			"score": student["score"]
		}
		if max_score == -1:
			max_score = student["score"]
		elif max_score > student["score"]:
			counter += 1
			max_score = student["score"]
		to_add["position"] = counter
		results += [to_add]
	return render_template("test/standings.html", results = results, test = test)
