#============================================#
#					     #
#		Mission Handeler             #
#					     #
#	      Author: davidkroell	     #
#					     #
#============================================#

import sys
import requests
import thread
from utils import Utils

sys.path.insert(0, "../interop/client/")
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
	def __init__(self, hst, prt, usr, pss):
		self.util = Utils()

		self.host = hst
		self.port = prt

		self.URIs = {}
		self.URIs['LOG'] = "/api/login"
		self.URIs['OBS'] = "/api/obstacles"
		self.URIs['TEL'] = "/api/telemetry"
		self.URIs['MIS'] = "/api/missions"

		self.componentsAvailable = False

		self.mission_components = {}

		self.mission_components['OBS'] = {}
		self.mission_components['WYP'] = {}
		self.mission_components['STI'] = {}
		self.mission_components['TAR'] = {}
		self.mission_components['FLZ'] = {}

		self.username = usr
		self.password = pss

		self.logged_in = False
		try:
			self.client = interop.Client( url=self.host+":"+self.port,
							username=self.username,
							password=self.password
							)
			self.logged_in = True
			self.util.succLog("Successfully logged into competition server.")

			self.util.log("Attempting to start Competition Server Retrieval Thread.")
			thread.start_new_thread(self.populateMissionComponents, ())
			self.util.succLog("Successfully started mission retrieval thread.")

		except interop.exceptions.InteropError:
			self.util.errLog("ERROR: Invalid login to competition server.")
		except requests.exceptions.ConnectionError:
			self.util.errLog("Connection error with competition server - Are you sure the Server is Running?")
			self.logged_in = False

	#==================
	#
	# Populates the mission components we need after each
	# time they are retrieved from the main task.
	#
	# Serves the purpose of synchronizing with mavlink thread module.
	#
	#==================
	def populateMissionComponents(self):
		while True:
			if not self.componentsAvailable:
				mission_data = self.getMissionData()[0]
				obstacle_data = self.getObstacles()

				# Update mission components

				self.mission_components['WYP'] = mission_data['mission_waypoints']
				self.mission_components['FLZ'] = mission_data['fly_zones']

				self.mission_components['TAR']['emergent_lastKnown'] = mission_data['emergent_last_known_pos']
				self.mission_components['TAR']['off_axis'] = mission_data['off_axis_target_pos']
				self.mission_components['TAR']['air_drop'] = mission_data['air_drop_pos']

				self.mission_components['OBS'] = obstacle_data

				self.componentsAvailable = True

	#========================
	#
	# Retrieves mission components from the mission class.
	# Triggers condition variable to allow for a new set to be retrieved.
	#
	#========================
	def getMissionComponents(self):
		if self.componentsAvailable:
			self.componentsAvailable = False
			return self.mission_components

	#===================
	#
	# Returns whether we're logged
	# into the competition server or not.
	#
	#===================
	def isLoggedIn(self):
		return self.logged_in

	#====================
	#
	# Grabs obstacle data from
	# interop server.
	#
	#====================
	def getObstacles(self):
		r = self.client.get(self.URIs['OBS'])
		return r.json()

	#========================
	# Post telemetry to the server.
	#
	#-------params:----------
	#	  lat - latitude value of plane.
	#	  lon - longitude value of plane.
	#	  alt - altitutde of the plane.
	#	  hdg - uas heading fo plane.
	#========================
	def postTelemetry(self, lat=38.145245, lon=-76.427946, alt=50, hdg=90):

		telemetry = interop.Telemetry(latitude=lat,
                              			longitude=lon,
                              			altitude_msl=alt,
                              			uas_heading=hdg
						)
		if (self.isLoggedIn()):
			self.client.post_telemetry(telemetry)

		self.mission_components['STI'] = self.client.get(self.URIs['TEL']).json()[len(self.client.get(self.URIs['TEL']).json())-1]['timestamp']


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
	def postTarget(self, typ='standard', lat=38.145215, lon=-76.427942, ori='n', shp='square',
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
	def getMissionData(self):
		r = self.client.get(self.URIs['MIS'])
		return r.json()


