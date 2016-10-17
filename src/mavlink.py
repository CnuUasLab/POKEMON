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


class Mavlink():
    def __init__(self, ip, port):
        self.target_ip   = ip
        self.target_port = port

        self.new_packet = None
        self.current_packet = ""

        thread.start_new_thread(startUDPStream, ())

    def startUDPStream(self):
        mav = mavutil.mavudp(self.ip+":"+self.port, ())
        while True:
            statusPacket = mav.recv()
            status = mav.recv_msg()
            if(status!=None):
                pass
    def getMavPacket(self):
        self.new_packet = None
        return self.current_packet
