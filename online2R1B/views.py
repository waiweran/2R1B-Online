from flask import render_template, request, redirect, session
from online2R1B import app, db, models

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
        if code.isalpha() and len(code) == 4 and models.Game.query.filter_by(code=code).first():
            return render_template('game.html', code=code)
        return render_template('game.html', code='')
    return redirect('/')


@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        while True:
            code = random.choice(letters) + random.choice(letters) + random.choice(letters) + random.choice(letters)
            if not models.Game.query.filter_by(code=code).first():
                break
        session['code'] = code
        db_game = models.Game(code=code, setup=pickle.dumps(json.loads(request.form['roles'])))
        db.session.add(db_game)
        db.session.commit()
        return redirect('/play')

    return render_template('create.html')


@app.route('/test/<toggle>/')
def test(toggle):
    return render_template('test.html', toggle=(toggle == 'true'))