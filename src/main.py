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

import json
import sys


util = Utils()

# Extract JSON data from configs.
with open('./config.json') as data_file:
	constants = json.load(data_file)

# Start Telemetry module to load data into.
telemetry = {}

util.succLog("Setting up mavlink recieving protocol - Instantiating modules...")


# Instantiate a Mavlink module.
mavl = Mavlink(
		constants['mavl-incoming']['host'],
		constants['mavl-incoming']['port']
	      )

#Instantiate Mission module.
miss = Mission(
		constants['auvsi']['host'],
		constants['auvsi']['port'],
		constants['auvsi']['username'],
		constants['auvsi']['password']
		)

# Grab mission/server data from the competition server.
missPacket = miss.getMissionComponents()

util.log("Ready to recieve Mavlink Packets...")
while True:
	try:
        	udpPacket = mavl.getMavPacket()
        	lonLatPacket = " "
        	if(udpPacket != None):

                	if (udpPacket.get_type() == "GLOBAL_POSITION_INT"):
                        	telemPacket = udpPacket

				# populate the longitude element of the telemetry module
				telemetry['longitude'] = float(telemPacket.lon)/10000000
				telemetry['latitude'] = float(telemPacket.lat)/10000000
				telemetry['heading'] = float(telemPacket.hdg)/1000
				telemetry['altitude'] = float(telemPacket.alt)/10000

				print telemetry
				# post telemetry to the Competition server.
				miss.postTelemetry(
							telemetry['latitude'],
							telemetry['longitude'],
							telemetry['altitude'],
							telemetry['heading']
					  	)
				if(missPacket != None):
					print missPacket

		missPacket = miss.getMissionComponents()

	except KeyboardInterrupt:
		break
