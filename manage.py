import sys

from online2R1B import app, db, socketio

if len(sys.argv) < 2:
	print('Commands: runserver, pubserver, setupdb')

elif sys.argv[1] == 'runserver':
	print('Running server')
	socketio.run(app, debug=True)

elif sys.argv[1] == 'pubserver':
	print('Publishing server')
	socketio.run(app, host='0.0.0.0', port=80)

elif sys.argv[1] == 'setupdb':
	print('Creating tables')
	with app.app_context():
		db.create_all()
