from flask import render_template, request, redirect, session, url_for
from online2R1B import app, db, models, cards

import random
import pickle
import json
import datetime


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form['code'].upper()
        if code.isalpha() and len(code) == 4 and models.Game.query.filter_by(code=code).first():
            session['code'] = code
            return redirect(url_for('play'))
        return redirect(url_for('index'))
    return render_template('index.html')


@app.route('/play/')
def play():
    if "code" in session:
        code = session['code']
        game_entry: models.Game = models.Game.query.filter_by(code=code).first()
        if code.isalpha() and len(code) == 4 and game_entry:
            return render_template('game.html', code=code, roles=pickle.loads(game_entry.setup), game_info=game_entry,
                                   cards=json.dumps(cards.allCards))
    return render_template('game.html', rejoin=True)


@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        while True:
            code = random.choice(letters) + random.choice(letters) + random.choice(letters) + random.choice(letters)
            if not models.Game.query.filter_by(code=code).first():
                break
        session['code'] = code
        setup = json.loads(request.form['roles'])
        num_players = request.form['numplayers']
        expandable = request.form['expand'] == 'true'
        db_game = models.Game(code=code, timestamp=datetime.datetime.now(), setup=pickle.dumps(setup),
                              min_players=num_players, expandable=expandable)
        db.session.add(db_game)
        db.session.commit()
        return redirect(url_for('play'))
    return render_template('create.html', cards=json.dumps(cards.allCards))


@app.route('/test/')
def test():
    session['test'] = True
    return redirect(url_for('create'))


@app.route('/stats/')
def stats():
    games = models.Game.query.with_entities(models.Game.timestamp,
                                            models.Game.min_players, models.Game.expandable).all()
    return render_template('stats.html', games=games, total=len(games))
