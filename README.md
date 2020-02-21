

# Note raspberry pi IP address is 
* #192.168.133.4
* 192.168.133.166

# First setup raspberry pi for passwordless ssh 
* See https://www.raspberrypi.org/documentation/remote-access/ssh/passwordless.md 
* Make sure you have an ssh key 
* Then do 
- ssh-copy-id <USERNAME>@<IP-ADDRESS>
- #ssh-copy-id pi@192.168.133.4
- ssh-copy-id pi@192.168.133.166

# Now working on setting up a separate config file 
* Basing off of https://sspinnovations.com/blog/python-best-practices-part-1/
* Lives in scripts_RPI
* run_default.cfg is the configuration file 
* configureRPI.py is the python script which picks it up and configures raspberry pi

# On the raspberry pi 
* To setup autoconfiguration, run
- python autoConfig.py
* This picks up changes to config.txt
* And runs 'python3 configureRPI.py' if there's a new configuration
* It also saves status to status.txt

# On the daq computer
* In scriptsDAQ directory, do
- python sendRPIConfig.py XXXX
* Where XXXX is the config number/name

# Misc
* to copy RPI code and config files to RPI 
- source copyRPI.sh 
