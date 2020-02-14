import time 
import os
import subprocess
import sys

def main():

    # Get config number
    config_number="default"
    if len(sys.argv) > 1 : config_number = sys.argv[1]
    
    # Raspberry Pi IP address and filepath
    pi_path="pi@192.168.133.4:~/Documents"
    
    # Setup File to Send
    config_file = "config.txt"
    f=open(config_file,"w")
    f.write(config_number)
    f.close()
    
    
    # Send config number to RPI
    bash_command = "scp {} {}/.".format(config_file,pi_path) 
    
    process = subprocess.Popen(bash_command.split(), 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    out,err = process.communicate()
    print(out)
    
    #for output in process.stdout.readlines():
    #    print(output.strip())
    
    # Wait to make sure config is picked up
    time.sleep(6)
    
    # Now read back status
    bash_command = "scp {}/status.txt .".format(pi_path)
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    for output in process.stdout.readlines():
        print(output.strip())
    
    f=open("status.txt","r")
    status = f.read().strip()
    f.close() 
    
    print("STATUS: {}".format(status))


if __name__ == "__main__":
     main()