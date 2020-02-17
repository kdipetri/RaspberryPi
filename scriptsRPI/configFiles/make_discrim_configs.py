import time 
import os
import subprocess
import sys

def bashProcess(command_string):

    process = subprocess.Popen(command_string.split(), 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

    for output in process.stdout.readlines():
        print(output.strip())

    return 

def makeConfigs(min_DAC=0,max_DAC=1000,step=100):
    
    # makes config files to scan 
    
    for i in range(min_DAC,max_DAC,step):
        
        cfg_name = "run_DAC_{}.cfg".format(i)

        # Copy default cfg 
        #bash_command = "cp run_default.cfg {}".format(cfg_name) 
        #bashProcess(bash_command)
        
    
        # Modify new file 
        fold=open("run_default.cfg","r+")
        fnew=open(cfg_name,"w+")
        for line in fold.readlines():
            if "DAC = " in line and "#" not in line: 
                fnew.write("DAC = {}".format(i))
            else : 
                fnew.write(line)
        fold.close()
        fnew.close()

        bash_command = "cp {}.tmp {}".format(cfg_name,cfg_name)
        bashProcess(bash_command)

        bash_command = "rm {}.tmp".format(cfg_name)
        bashProcess(bash_command)
    

makeConfigs()
