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

# Grab obstacle/server data from the competition server.
mission_data = miss.getMissionData()
server_data = miss.getServerData()

print mission_data
print "--------------------------------------------"
print server_data
util.log("Ready to recieve Mavlink Packets...")
while True:
	try:
        	currPacket = mavl.getMavPacket()
        	lonLatPacket = " "
        	if(currPacket != None):

                	if (currPacket.get_type() == "GLOBAL_POSITION_INT"):
                        	lonLatPacket = currPacket

				# populate the longitude element of the telemetry module
				telemetry['longitude'] = float(lonLatPacket.lon)/10000000
				telemetry['latitude'] = float(lonLatPacket.lat)/10000000
				telemetry['heading'] = float(lonLatPacket.hdg)/1000
				telemetry['altitude'] = float(lonLatPacket.alt)/10000

				print telemetry
				# post telemetry to the Competition server.
				miss.postTelemetry(
							telemetry['latitude'],
							telemetry['longitude'],
							telemetry['altitude'],
							telemetry['heading']
					  	)
		# Update mission data constantly.
		mission_data = miss.getMissionData()	# --> This is not optimized. Chewing up frequency time...
               	#server_data = miss.getServerData()

	except KeyboardInterrupt:
		break
