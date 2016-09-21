#=====================================================#
#  This is the main script for the Interoperability
#
#      Author: vixadd
#      Date: 09/19/2016
#
#=====================================================#


import json

# Load JSON data from config file
with open('./config.json') as data_file:
    data = json.loads(data_file.read().replace("\n", ""))
