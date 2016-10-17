import socket
from pymavlink import mavutil

mav = mavutil.mavudp("137.155.41.65:14550", input=True)
while True:
	status = mav.recv_msg()
	if(status!=None):
		print status
