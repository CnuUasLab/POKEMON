import socket
from pymavlink import mavutil

UDP_Location = "127.0.0.1:14550"

mav = mavutil.mavudp(UDP_Location, input=True)
while True:
	status = mav.recv_msg()
	if(status!=None):
		print status
