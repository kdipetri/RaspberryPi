

# Note raspberry pi IP address is 
* 192.168.133.4

# First setup raspberry pi for passwordless ssh 
* See https://www.raspberrypi.org/documentation/remote-access/ssh/passwordless.md 
* Make sure you have an ssh key 
* Then do 
- ssh-copy-id <USERNAME>@<IP-ADDRESS>
- ssh-copy-id ssh pi@192.168.133.4

# Now working on setting up a separate config file 
* Basing off of https://sspinnovations.com/blog/python-best-practices-part-1/
* run_default.cfg is the configuration file 
* configureRPI.py is the python script which picks it up and configures raspberry pi
