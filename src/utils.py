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

class Singleton(type):
	def __init__(cls, string, extra, what):
		super(Singleton, cls).__init__(string)
		cls.instance = None

	def __call__(cls, *args, **kwargs):
		if cls.instance is None:
			print "Creating NEW instance"
			cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
		else:
			print "Using EXISTING instance"
		return cls.instance	



class Utils(object):

	__metaclass__ = Singleton

	def __init__(self, arg = None):
		print "creating instance with arg: ", arg
		self.logs = []
		self.currLog = 'Initialized'

	def log(self, string):
		print bcolors.BOLD + string + bcolors.ENDC
		self.currLog = string
		self.logs.append(string)

	def errLog(self, string):
		print bcolors.ERROR + string + bcolors.ENDC
		self.currLog = string
		self.logs.append(string)

	def succLog(self, string):
		print bcolors.SUCCESS + string + bcolors.ENDC
		self.currLog = string
		self.logs.append(string)

	def getPreviousLogs(self):
		return self.logs

	def dump(self):
		f = open("./dumpFile.txt","w+")
		for word in self.getPreviousLogs():
			f.write(word)

# creates a new instance of Utils
x = Utils("Something")
x.log("error")

print('\n')

# since object exists, no need to create a new one
# instead, use the existing instance of Utils
y = Utils("DJ KHALED")
y.log("WE THE BEST")