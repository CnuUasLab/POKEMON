#===============================================================#
#								#
#			Mavlink Library				#
#								#
#			Author: davidkroell    			#
#			Version: 2016-10-03			#
#								#
#	     This is the mavlink library that is used		#
#	  to send and recieve mavlink data from/to the plane.	#
#								#
#===============================================================#

from pymavlink import mavlinkv11 as mavlink
from pymavlink import mavutil

import json
import socket
import thread

#====================
# Mavlink module class. Creates new instance of Mavlink Module
#
# ip: - Is the hostname of the place recieving packets.
# port - Is the port on which you recieve packets. (usually 14550)
#====================
class Mavlink():
    def __init__(self, ip, port):
        self.target_ip   = ip
        self.target_port = port

        self.new_packet = None
        self.current_packet = ""

        self.mav = mavutil.mavudp(self.target_ip+":"+self.target_port, ())

        thread.start_new_thread(self.startUDPStream, ())

    # Function called in the thread to constantly update packets.
    def startUDPStream(self):
        while True:
            #	statusPacket = mav.recv()
            status = self.mav.recv_msg()
            if(status!=None and not(self.new_packet)):
                self.new_packet = True
		self.current_packet = status

    # Accessor, to get the current packet
    def getMavPacket(self):
        if(self.newPacketAvailable()):
            self.new_packet = None
            return self.current_packet

    # Fucntion to return whether there is a new packet available
    def newPacketAvailable(self):
        return self.new_packet

    # Posts data to the airplane.
    def postData(self, packet):
        '''
        We gotta figure out how to do this.
        I'm researching it.
        '''
        pass
