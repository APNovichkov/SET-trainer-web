from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from settrainer import SetTrainer

app = Flask(__name__)

client = MongoClient()
settrainer = client['settrainer']
games = settrainer['games']
sessions = settrainer['sessions']
questions = settrainer['questions']


set_trainer = SetTrainer()


@app.route("/")
def setup():
	"""Setups session and redirect to welcome page."""

	session = {'timestamp': datetime.now()}
	session_id = str(sessions.insert_one(session).inserted_id)

	return redirect(url_for('welcome_function', session_id=session_id))


@app.route('/welcome/<session_id>')
def welcome_function(session_id):
	"""Show welcome page with settings and instructions on trainer."""

	print("This is the session id: {}".format(session_id))

	return render_template("welcome.html", session_id=ObjectId(session_id))


@app.route('/welcome/<session_id>', methods=['POST'])
def setup_game(session_id):

	num_rounds = int(request.form.get("numrounds"))

	game = {
		'session_id': session_id,
		'num_rounds': num_rounds
	}

	game_id = str(games.insert_one(game).inserted_id)

	generated_questions = set_trainer.get_cards(num_rounds)

	first_question_id = None

	for i in range(len(generated_questions)):
		print("i: {}".format(i))
		print('shape: {}'.format(generated_questions[i].shape))
		print('color: {}'.format(generated_questions[i].color))
		question = {
			'game_id': game_id,
			'index': i,
			'shape': generated_questions[i].shape,
			'color': generated_questions[i].color,
			'shade': generated_questions[i].shade,
			'number': generated_questions[i].number,
		}

		if i == 0:
			first_question_id = str(questions.insert_one(question).inserted_id)
		else:
			questions.insert_one(question)

	return redirect(url_for(
		"game_function",
		session_id=session_id,
		game_id=game_id,
		question_id=first_question_id))


@app.route('/game/<session_id>/<game_id>/<question_id>')
def game_function(session_id, game_id, question_id):
	"""Show the game page."""

	return render_template(
		"game.html",
		session_id=session_id,
		game_id=game_id,
		question=questions.find_one({'_id': ObjectId(question_id)}))


@app.route('/game/<session_id>/<game_id>/<question_id>/next')
def next_set_function(session_id, game_id, question_id):
	"""Show the next game card or stats of game is over."""

	c_game = games.find_one({'_id': ObjectId(game_id)})
	c_question = questions.find_one({'_id': ObjectId(question_id)})

	# If game over
	if c_game['num_rounds'] - 1 == c_question['index']:
		return redirect(url_for('stats_function'))

	# If game goes on
	return redirect(url_for(
		"game_function",
		session_id=session_id,
		game_id=game_id,
		question_id=questions.find_one({'index': c_question['index'] + 1})['_id']))


@app.route('/stats')
def stats_function():
	"""Shows Stats for the current game and other relative information."""

	return render_template('stats.html')



@app.route('/game/choice/<card_id>', methods=['POST'])
def card_choice_function():
	"""Update user choice on current set of cards."""

	pass


if __name__ == "__main__":
	app.run(debug=True)
