#!/usr/bin/python

from flask import Flask, render_template, session, request, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

import json
import thread
import sys
import time

sys.path.insert(0, "../src/")
from utils import Utils
from mav import Mavlink
from mission import Mission


# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None

util = Utils()

try:
        # Extract JSON data from configs.
        with open('../src/config.json') as data_file:
                constants = json.load(data_file)
        util.succLog("Successfully extracted config data")

except IOError:
        util.errLog("WARNING: Config file not found!")
        util.errLog("Aborting operation! Make sure config.json exists in the /src directory.")
        util.errLog("I'm angry so I'm going to dump everything into dumpFile.txt now! GoodBye!!!")
#       util.dump() - > Being developed.
        sys.exit(0)

# Start Telemetry module to load data into.

mavl = Mavlink(
                constants['mavl-incoming']['host'],
                constants['mavl-incoming']['port']
              )


miss = Mission(
                constants['auvsi']['host'],
                constants['auvsi']['port'],
                constants['auvsi']['username'],
                constants['auvsi']['password']
                )

def postTelem(telemetry):
        global packets_sent
        # post telemetry to the Competition server.
        miss.postTelemetry(
                telemetry['latitude'],
                telemetry['longitude'],
                telemetry['altitude'],
                telemetry['heading']
        )
        packets_sent += 1
        
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
# Background thread to be run when
# a client connects to the server being hosted.
#
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
def background_thread():
	"""Example of how to send server generated events to clients."""

	count = 0
	telemetry = {}
	util.log("Hello - Websocketing thread initiated")
	socketio.sleep(0)

        packets_sent = 0
        startTime = time.time()
        
	"""Example of how to send server generated events to clients."""
	while True:
                
        #        print "loop"
		udpPacket = mavl.getMavPacket()
		lonLatPacket = " "
		if(udpPacket != None):
			if(udpPacket.get_type() == "GLOBAL_POSITION_INT"):
				socketio.sleep(1)
				#util.log("GLOBAL_POSITION_INT: Packet Recieved")

				telemPacket = udpPacket

				# populate the longitude element
				telemetry['longitude'] = float(telemPacket.lon)/10000000
				telemetry['latitude'] = float(telemPacket.lat)/10000000
				telemetry['heading'] = float(telemPacket.hdg)/100
				telemetry['altitude'] = float(telemPacket.alt)/10000

#                                print system_time
                                
				socketio.emit('tele', {'data': telemetry, 'count': count}, namespace='/test')
				socketio.emit('srvTime', {'data': str(miss.getSystemTime()), 'count': count}, namespace='/test')

                                if (miss.isLoggedIn()):
#                                       thread.start_new_thread(postTelem, (telemetry,))
                                        postTelem(telemetry)
#                                       print telemetry

                                #socketio.sleep(10)
				count += 1

                                miss_packet = miss.getMissionComponents()
                                if(miss_packet != None):
#                                        print miss_packet
                                        
                                        obstacle = miss_packet['OBS']
                                        waypoints = miss_packet['WYP']
                                        targets = miss_packet['TAR']
                                        socketio.emit('obs', {'data': obstacle, 'count': count}, namespace='/test')
                                        socketio.emit('wyp', {'data': waypoints, 'count': count}, namespace='/test')
                                        socketio.emit('tar', {'data': targets, 'count': count}, namespace='/test')
                                        #socketio.emit('srvTime', {'data': str(miss_packet.getSystemTime()), 'count': count}, namespace='/test')
                                        
                        # Recalculate the number of seconds elapsed
                        elapsed = time.time() - startTime

                        # If one second has elapsed reset the clock and print the frequency.
                        if elapsed >= 1:
                                global packets_sent
                                telemetry['frequency'] = packets_sent
#                                print telemetry['frequency']
                                startTime = time.time()
                                packets_sent = 0
@app.route('/')
def index():
	return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/status')
def status():
	return render_template('status.html', async_mode=socketio.async_mode)
#@app.route('/js/OpenLayers')
#def ol2():
#        return send_from_directory('js', './ol2/lib/OpenLayers.js')

#@app.route('/js/map')
#def map():
#        return send_from_directory('js', './map_app/app.js')

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
