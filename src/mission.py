import sys

sys.path.insert(0, "../interop/client")
import interop

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
