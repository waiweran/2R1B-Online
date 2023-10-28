from flask import render_template, request, redirect, session, url_for
from online2R1B import app, db, models, cards

import random
import pickle
import json
import datetime


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Used to display home page
    Accepts Post requests creating new games
    :return:
    """
    if request.method == 'POST':
        code = request.form['code'].upper()
        if code.isalpha() and len(code) == 4:
            game_entry = models.Game.query.filter_by(code=code).first()
            if game_entry:
                return redirect(url_for('play', game_id=game_entry.id))
        return redirect(url_for('index'))
    return render_template('index.html')


@app.route('/<game_id>/')
def play(game_id):
    """
    Displays the main game and join screen
    :param game_id: database ID of the game
    :return:
    """
    game_entry: models.Game = models.Game.query.get(game_id)
    if game_entry:
        if not game_entry.object:
            return render_template('game.html', roles=pickle.loads(game_entry.setup), game_info=game_entry)
        else:
            return render_template('game.html', rejoin=True, game_info=game_entry)
    return redirect(url_for('index'))


@app.route('/create/', methods=['GET', 'POST'])
def create():
    """
    Displays game creation role selection page
    Accepts Post requests to finalize role selection and create game
    :return:
    """
    if request.method == 'POST':
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        while True:
            code = random.choice(letters) + random.choice(letters) + random.choice(letters) + random.choice(letters)
            if not models.Game.query.filter_by(code=code).first():
                break
            else:
                game_conflict: models.Game = models.Game.query.filter_by(code=code).first()
                if datetime.datetime.now() - game_conflict.timestamp > datetime.timedelta(days=2):
                    game_conflict.code = None
                    break

        setup = json.loads(request.form['roles'])
        num_players = request.form['numplayers']
        expandable = request.form['expand'] == 'true'
        db_game = models.Game(code=code, timestamp=datetime.datetime.now(), setup=pickle.dumps(setup),
                              min_players=num_players, expandable=expandable)
        db.session.add(db_game)
        db.session.commit()
        return redirect(url_for('play', game_id=db_game.id))
    return render_template('create.html', cards=json.dumps(cards.allCards))


@app.route('/test/')
def test():
    """
    Sets testing variable and redirects to game creation page
    :return:
    """
    session['test'] = True
    return redirect(url_for('create'))


@app.route('/stats/')
def stats():
    """
    Displays site usage stats page
    :return:
    """
    games = models.Game.query.with_entities(models.Game.timestamp,models.Game.min_players,
                                            models.Game.expandable, models.Game.started, models.Game.ended).all()
    return render_template('stats.html', games=games, total=len(games))
