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

def makeConfigs(DAC=200):
    
    # makes config files to scan 
     
    for power in ["0b111", "0b000"]:
        for gain in range(0,4):
        
            cfg_name = "run_IBSel_{}_RFSel_{}_DAC_{}.cfg".format(power,gain,DAC)

            # Copy default cfg 
            #bash_command = "cp run_default.cfg {}".format(cfg_name) 
            #bashProcess(bash_command)
            
    
            # Modify new file 
            fold=open("run_default.cfg","r+")
            fnew=open(cfg_name,"w+")
            for line in fold.readlines():
                if "DAC = " in line and "#" not in line: 
                    fnew.write("DAC = {}".format(DAC))
                elif "IBSel = " in line and "#" not in line: 
                    fnew.write("IBSel = {}".format(power))
                elif "RFSel = " in line and "#" not in line: 
                    fnew.write("RFSel = {}".format(gain))
                else : 
                    fnew.write(line)
            fold.close()
            fnew.close()


    return 

makeConfigs()
