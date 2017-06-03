import os

class bcolors:
		HEADER = '\033[95m'
		OKBLUE = '\033[94m'
		OKGREEN = '\033[92m'
		WARNING = '\033[93m'
		FAIL = '\033[91m'
		ENDC = '\033[0m'
		BOLD = '\033[1m'
		SUCCESS = '\033[1;42m'
		UNDERLINE = '\033[4m'
		ERROR = '\033[1;41m'

# Using this as a Template
"""
class Singleton:
	def __init__(self, decorated):
		self.logs = []
		self._decorated = decorated

	def Instance(self):
		try:
			return self._instance
		except AttributeError:
			self._instance = self._decorated
			return self._instance

	def __call__(self):
		raise TypeError('Singletons must be accessed through `Instance()`.')

	def __instancecheck__(self, inst):
		return isinstance(inst, self._decorated)
"""


def b_colors(myClass):
	instances = {}
	def getColor(first, string, second):
		if myClass not in instances:
			instances[myClass] = myClass(first, string, second)
			print instances[myClass]
		return instances[myClass]
	return getColor


@b_colors
class Utils(bcolors):
	def __init__(self, string):
		print 'Instance created'

	def log(self, string):
#		print bcolors.BOLD + string + bcolors.ENDC
		x = getColor(BOLD, string, ENDC)
		print x
		self.currLog = string
		self.logs.append(string)

	def errLog(self, string):
#		print bcolors.ERROR + string + bcolors.ENDC
		getColor(ERROR, string, ENDC)

		self.currLog = string
		self.logs.append(string)

	def succLog(self, string):
#		print bcolors.SUCCESS + string + bcolors.ENDC
		getColor(SUCCESS, string, ENDC)

		self.currLog = string
		self.logs.append(string)

	def getPreviousLogs(self):
		return self.logs

	def dump(self):
		f = open("./dumpFile.txt","w+")
		for word in self.getPreviousLogs():
			f.write(word)

x = Utils()
x.log('Something')