#=======================================================#
# Main class for handeling Interoperability operations. #
#                                                       #
#             Author: davidkroell                       #
#             Version: 0.0.1                            #
#=======================================================#

from mav import Mavlink
import json
import sys


# Extract JSON data from configs.
with open('./config.json') as data_file:
	constants = json.load(data_file)

# Instantiate a Mavlink module.
mavl = Mavlink(constants['mavl-incoming']['host'], constants['mavl-incoming']['port'])

while True:
        currPacket = mavl.getMavPacket()
        if(currPacket != None):
                # post data to competition server
                # Notify that a packet has been recieved
                # post data to the socket server for Electron
                pass
        # Update Obstacle Data
