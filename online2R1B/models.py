from online2R1B import db


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    game = db.relationship('Game', backref=db.backref('players', lazy=True))


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, unique=True)
    setup = db.Column(db.PickleType, nullable=False)
    object = db.Column(db.PickleType)


