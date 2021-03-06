# POKEMON
<b>P</b>ython <b>O</b>n <b>K</b>omputers for <b>E</b>nhanced <b>M</b>anagement <b>O</b>ver <b>N</b>etworks

## Synopsis
This is the project for managing the interoperability of the plane. The majority of the project is python based, due
to the nature of the competition server's python based API.

## Developers
The main script that is used for mavlink recieve and broadcast is <b>Python 2.7</b>
Currently there are no procedures for Python 3 and above, so it is essential to use Python 2.7 at this time.
The front end of the application is to be built using an electron based build.
### Setup
Make sure you have the python dev packages availble:
sudo apt-get install python-dev
sudo apt-get install python-pip

You should be able to install everything from the requirements list run:
</br>`sudo pip install -r requirements.txt`

You also need to update the competition's interoperability competition server repository so that we can use their client tools:
</br> `git submodule init`
</br> `git submodule update`

Inorder to gain interface access to the electron module, you will need to install all
packages regarding electron.
You can execute this with the following command:
` sudo npm install -g`

### Automated Testing
Main automation testing is done through Software in the Loop (SITL)
When you execute SITL, load the main Waypoint data, and then run.
Find your ip address on your computer by typing `ifconfig` in command line.

The program in it's entirety can be run with the initiation script:
`./startPOKEMON`

The IP address needs to be added to SITL's output by adding it through `output add <ipaddr>:14550`
When you Add that and then run: `cd src && python main.py` the command should run.

