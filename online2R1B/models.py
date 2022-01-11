from online2R1B import db


class Player(db.Model):
    sid = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(15))
    ready = db.Column(db.Boolean, default=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    game = db.relationship('Game', backref=db.backref('players', lazy=True))


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(4), unique=True)
    timestamp = db.Column(db.DateTime)
    setup = db.Column(db.PickleType)
    min_players = db.Column(db.Integer)
    expandable = db.Column(db.Boolean)
    object = db.Column(db.PickleType)


