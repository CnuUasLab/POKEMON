import socket
from pymavlink import mavutil

mav = mavutil.mavudp("0.0.0.0:14550", input=True)
while True:
	status = mav.recv_msg()
	if(status!=None):
		print status
