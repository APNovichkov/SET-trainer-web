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
	session_id = sessions.insert_one(session).inserted_id

	return redirect(url_for('welcome_function', session_id=session_id))


@app.route('/welcome/<session_id>')
def welcome_function(session_id):
	"""Show welcome page with settings and instructions on trainer."""

	print("This is the session id: {}".format(session_id))

	return render_template("welcome.html", session_id=session_id)


@app.route('/welcome/<session_id>', methods=['POST'])
def setup_game(session_id):

	num_rounds = int(request.form.get("numrounds"))

	game = {
		'session_id': session_id,
		'num_rounds': num_rounds
	}

	game_id = games.insert_one(game).inserted_id

	generated_questions = set_trainer.get_cards(3)

	for i in range(len(generated_questions)):
		question = {
			'game_id': game_id,
			'index': i,
			'shape': generated_questions[i].shape,
			'color': generated_questions[i].color,
			'shade': generated_questions[i].shade,
			'number': generated_questions[i].number,
		}

		questions.insert_one(question)

	return render_template("game.html", game_id=game_id, question=questions.find_one({'index': 0}))


@app.route('/game')
def game_function():
	"""Shows the game page."""

	pass

@app.route('/stats')
def stats_function():
	"""Shows Stats for the current game and other relative information."""

	pass

@app.route('/game/next')
def next_set_function():
	"""Show the next game card or stats of game is over."""

	pass

@app.route('/game/choice/<card_id>', methods=['POST'])
def card_choice_function():
	"""Update user choice on current set of cards."""

	pass


if __name__ == "__main__":
	app.run(debug=True)
