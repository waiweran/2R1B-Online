import sys

from online2R1B import app, db, socketio

if len(sys.argv) < 2:
	print('Commands: runserver, setupdb')

elif sys.argv[1] == 'runserver':
	print('Running server')
	socketio.run(app, debug=True)

elif sys.argv[1] == 'setupdb':
	print('Creating tables')
	with app.app_context():
		db.create_all()