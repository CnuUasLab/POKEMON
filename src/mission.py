#============================================#
#					     #
#		Mission Handeler             #
#					     #
#	      Author: davidkroell	     #
#					     #
#============================================#

import sys

sys.path.insert(0, "../interop/client")
import interop

#==================================
#
# Missions module for each mission.
#
#------params:---------------------
#	hst - hostname/ipaddr
#	prt - port that the competition sever runs on.
#	usr - Username for the server
#	pss - Password for the server
#
#==================================
class Mission():
	def __init__(hst, prt, usr, pss):
		self.host = hst
		self.port = prt

		self.URIs = {}
		self.URIs['LOG'] = "/login"
		self.URIs['OBS'] = "/obstacles"
		self.URIs['TEL'] = "/telemetry"

		self.username = usr
		self.password = pss

		self.client = interop.Client( url=self.host+":"+self.port
						username=self.username
						password=self.password
						)

		
	#========================
	# Post telemetry to the server.
	# 
	#-------params:----------
	#	  lat - latitude value of plane.
	#	  lon - longitude value of plane.
	#	  alt - altitutde of the plane.
	#	  hdg - uas heading fo plane.
	#========================
	def postTelemetry(lat=38.145245, lon=-76.427946, alt=50, hdg=90):
		
		telemetry = interop.Telemetry(latitude=lat,
                              			longitude=lon,
                              			altitude_msl=alt,
                              			uas_heading=hdg
						)

		self.client.post_telemetry(telemetry)

	#=============================
	# 	   Post a detected target on
	#	the field through the SIRE module.
	#
	#-------params:---------------
	#	  typ - The type of target
	#	  lat - latitude location of the target
	#	  lon - longitude location of the target
	#	  ori - Orientation of the target
	#	  shp - Shape of the target
	#	  bgc - background color of the taget
	#	  letter - Letter printed on the front of the target
	#	  color - color of the target text.
	#	  image_path - path of the image where target is found.
	#============================
	def postTarget(typ='standard', lat=38.145215, lon=-76.427942, ori='n', shp='square',
				 bgc='green', letter='A', color='white', image_path='~/image.png'):
		
		target = interop.Target(type=typ,
                        latitude=lat,
                        longitude=lon,
                        orientation=ori,
                        shape=shp,
                        background_color=bgc,
                        alphanumeric=letter,
                        alphanumeric_color=color)

		target = client.post_target(target)

		with open(image_path, 'rb') as f:
    			image_data = f.read()
    			self.client.put_target_image(target.id, image_data)

	#==========================
	# 
	# Retrieve the mission data for the competition. 
	#
	#==========================
	def getMissionData():
		return self.client.get_missions
	
	#==========================
	#
	# Retrieve obstacles for the mission.
	#
	#==========================
	def getObstacles():
		return self.client.get_obstacles()


