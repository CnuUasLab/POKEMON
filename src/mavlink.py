#===============================================================#
#								#
#			Mavlink Library				#
#								#
#			Author: vixadd				#
#			Version: 2016-10-03			#
#								#
#	     This is the mavlink library that is used		#
#	  to send and recieve mavlink data from/to the plane.	#
#								#
#===============================================================#

from pymavlink import mavlinkv11 as mavlink
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
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, UDP_PORT))
        while True:
            data, addr = sock.recvfrom(1024)
            
            self.curent_packet = data
            self.new_packet = True

    def getCurrentMavPacket(self):
        self.new_packet = None
        return self.current_packet
    

        
