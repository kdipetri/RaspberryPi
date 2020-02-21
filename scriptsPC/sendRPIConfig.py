import time 
import os
import subprocess
import sys

def sendRPIConfig(config_number):

    
    # Raspberry Pi IP address and filepath
    pi_path="pi@192.168.133.166:~/Documents"
    #pi_path="pi@192.168.133.4:~/Documents"

    # Setup files to Send
    config_file = "config.txt"
    f=open(config_file,"w")
    f.write(config_number)
    f.close()
    
    bash_command = "scp {} {}/.".format(config_file,pi_path) 

    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    for output in process.stdout.readlines():
        print(output.strip())
    
    # Wait to make sure config is picked up
    time.sleep(3)
    
    # Now read back status
    bash_command = "scp {}/status.txt .".format(pi_path)
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    for output in process.stdout.readlines():
        print(output.strip())
    
    f=open("status.txt","r")
    status = f.read().strip()
    f.close() 
    
    print("STATUS: {}".format(status))

def main():
    config_number="default"
    if len(sys.argv) > 1 : config_number = sys.argv[1]

    sendRPIConfig(config_number)


if __name__ == "__main__":
    main()
