#===============================================#
#						#
#	Front end Back end controller for	#
#		html componenets		#
#						#
#	      Author: davidkroell		#
#						#
#	      Version: 2017-05-08		#
#						#
#===============================================#


from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, disconnect
import sys
import json

sys.path.insert(0, "../src/")
from mav import Mavlink
from utils import Utils

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


async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None


def background_thread():
	"""Example of how to send server generated events to clients."""
	count = 0
	while True:
		socketio.sleep(10)
		count += 1
		###################### You know what to do #########################


@app.route('/')
def index():
	return render_template('index.html', async_mode=socketio.async_mode)


@app.route('/console')
def console():
	return render_template('console.html', async_mode=socketio.async_mode)

if __name__ == '__main__':
	socketio.run(app, debug=True)
