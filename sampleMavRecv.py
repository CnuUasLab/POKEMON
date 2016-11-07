import socket
import time
from pymavlink import mavutil

mav = mavutil.mavudp("0.0.0.0:14550", input=True)
while True:
	try:
		status = mav.recv_msg()
		#print "< ------------------------------------------------------------------------------------- >"
		if(status!=None and status.get_type()=="GLOBAL_POSITION_INT"):
		#	print "lon: "+str(float(status.lon)/10000000)+" lat: "+str(float(status.lat)/10000000)+" "+str(time.time())
	except KeyboardInterrupt:
		break
