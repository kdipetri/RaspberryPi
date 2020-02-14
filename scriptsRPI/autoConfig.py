import time 
import os
import subprocess

debug = False 

time_step = 5

path_rpi = "/home/pi/Documents" 
path_daq = "/home/daq/RaspberryPi/scriptsRPI" 


if debug : path = path_daq
else     : path = path_rpi

# Setup infinite loop 
config_input = "{}/config.txt".format(path)
config_status = "{}/status.txt".format(path)

print("Reading config from {}".format(config_input)) 

prev_config = "default"
while True:


    config_name = open(config_input,'r').readline().strip()

    if config_name!=prev_config:

        config_file = "{}/configFiles/run_{}.cfg".format(path,config_name)

        print("Going to use configuration: {}".format(config_file))

        # Check to make that configuration makes sense
        if os.path.isfile(config_file) :

            print("Config File exists!")

            # configure ETROC
            bash_command = "python3 configureRPI.py {}".format(config_file) 
            
            process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)

            for output in process.stdout.readlines():
                print(output.strip())

     
            # update prev_config
            prev_config = config_name

        # If config doesn't exist use previous config and spit out an error
        else : 
            print("Config File doesn't exist!")
            print("Continue using previous config: run_{}.cfg".format(prev_config))
            fout = open(config_status,'w')  
            fout.write("MISSING_CONFIG")
            fout.close()
            
    
    
    print("Going to sleep for {} seconds".format(time_step))
    time.sleep(time_step)
