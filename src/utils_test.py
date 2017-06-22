#!/bin/python

#=======================================================#

# Main class for handeling Interoperability operations. #

#                                                       #

#                Author: davidkroell                    #

#                  Version: 0.0.1                       #

#=======================================================#



from mav import Mavlink

from mission import Mission

from utils import Utils

from flask import Flask, render_template

from flask_socketio import SocketIO



import thread

import json

import sys

import time



util = Utils()



try:

	# Extract JSON data from configs.

	with open('./config.json') as data_file:

		constants = json.load(data_file)

	util.succLog("Successfully extracted config data")



except IOError:

	util.errLog("WARNING: Config file not found!")

	util.errLog("Aborting operation! Make sure config.json exists in the /src directory.")

	util.errLog("I'm angry so I'm going to dump everything into dumpFile.txt now! GoodBye!!!")

#	util.dump() - > Being developed.

	sys.exit(0)



# Start Telemetry module to load data into.

telemetry = {}



util.succLog("Setting up mavlink recieving protocol - Instantiating modules...")





# Instantiate a Mavlink module.

mavl = Mavlink(

		constants['mavl-incoming']['host'],

		constants['mavl-incoming']['port']

	      )



# Instantiate Mission module.

miss = Mission(

		constants['auvsi']['host'],

		constants['auvsi']['port'],

		constants['auvsi']['username'],

		constants['auvsi']['password']

		)



# Grab mission/server data from the competition server.

missPacket = miss.getMissionComponents()



packets_sent = 0

startTime = time.time()



# Starting front end components.

util.log("Initiating telemetry status console front end")



util.log("Ready to recieve Mavlink Packets...")
