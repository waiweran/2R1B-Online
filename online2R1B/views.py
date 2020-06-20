from flask import render_template, request, redirect, session
from online2R1B import app, db, models, cards

import random
import pickle
import json


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form['code'].upper()
        if code.isalpha() and len(code) == 4 and models.Game.query.filter_by(code=code).first():
            session['code'] = code
            return redirect('/play')
        return redirect('/')
    return render_template('index.html')


@app.route('/play/')
def play():
    if "code" in session:
        code = session['code']
        game_entry: models.Game = models.Game.query.filter_by(code=code).first()
        if code.isalpha() and len(code) == 4 and game_entry:
            return render_template('game.html', code=code, game_info=game_entry)
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
        db_game = models.Game(code=code, setup=pickle.dumps(setup), min_players=num_players, expandable=expandable)
        db.session.add(db_game)
        db.session.commit()
        return redirect('/play')

    return render_template('create.html', cards=json.dumps(cards.allCards))


@app.route('/test/<toggle>/')
def test(toggle):
    return render_template('test.html', toggle=(toggle == 'true'))
