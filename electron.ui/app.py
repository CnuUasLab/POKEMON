#!/usr/bin/env python
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None


def background_thread():
	"""Example of how to send server generated events to clients."""
	count = 0
	telemetry = {}

	"""Example of how to send server generated events to clients."""
	while True:
		socketio.sleep(10)

		udpPacket = mavl.getMavPacket()
		lonLatPacket = " "
		if(udpPacket != None):
			if(udpPacket.get_type() == "GLOBAL_POSITION_INT"):
				telemPacket = udpPacket

				# populate the longitude element
				telemetry['longitude'] = float(telemPacket.lon)/10000000
				telemetry['latitude'] = float(telemPacket.lat)/10000000
				telemetry['heading'] = float(telemPacket.hdg)/1000
				telemetry['altitude'] = float(telemPacket.alt)/10000

                                system_time = miss.getMissionTime()

				socketio.emit('tele',
				              {'data': telemetry, 'count': count},
				                namespace='/test')
				socketio.emit('srvTime',
				              {'data': server_time, 'count': count},
				                namespace='/test')
                                print system_time

				socketio.sleep(10)
				count += 1
				


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, debug=True)
