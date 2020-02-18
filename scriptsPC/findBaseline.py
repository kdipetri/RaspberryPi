import sys
sys.path.append('/home/daq/BiasScan/ETLSBSF/')
sys.path.append('/home/daq/RaspberryPi/scriptsPC/')

from acquisition_wrapper_DACscan import * 
from sendRPIConfig import sendRPIConfig

import time 

run_number=-1

def doRun(nevents,max_time):
	# Take a scan 
	# nevents = total number of events
	# max_time = maximum time before timeout (in seconds)
	ScopeAcquisition(run_number, nevents, max_time)


	# come back to this later
	#os.system(AgilentScopeCommand)
	return 

def getRate():

	f=open("tmp.txt","r")
	line = f.readline()
	rate = line.split("Trigger rate: ")[1]

	print(rate)

	return rate

# Do a one event run for 1 second

# If you have an event 
# DO a second run for more events
# Get the rate 

min_DAC = 165
max_DAC = min_DAC+20

power="0b111" # low power
#power="0b000" # high power

gain=3 # low gain
#gain=0 # high gain

fout=open("thresholdScan.txt","w")

start_time = time.time()

max_rate = 0

DAC = min_DAC
while DAC < max_DAC: 

	# Configure RPI
	sendRPIConfig("IBSel_{}_RFSel_{}_DAC_{}".format(power,gain,DAC))

	# Do a one event run for 1 second
	ScopeAcquisition(run_number, 1, 1)
	

	rate = getRate()

	if "unknown" not in rate: # found events

		# Do a test run 
		ScopeAcquisition(run_number, 10,1.1)
		# time to record 10 events limited by acquisiton script?

		rate_1 = getRate()

		if "unknown" not in rate_1: # found events

			# Do a test run 
			ScopeAcquisition(run_number, 1000,100)
			# time to record 10 events limited by acquisiton script?

			rate_2 = getRate()

			if "unknown" not in rate_2:
				rate = rate_2
			else :
				rate = rate_1 

		else : 
			rate = rate
		


	# Print rate info to screen	
	print("DAC {} : rate {}".format(DAC, rate))

	# Save rate info
	fout.write("DAC {} : rate {} ".format(DAC, rate))


	# Conditions to speed up process
	if "unknown" not in rate: 
		rate_float = float(rate.split()[0])
		
		if rate_float < 10 : DAC = DAC + 2# step by 2
		else : DAC = DAC + 1

		if rate_float > max_rate : 
			max_rate = rate_float
		if max_rate > 1000 and rate_float < max_rate/10.: # We found baseline, and are passed it, finish stepping
			break 
	
	else : 
		DAC = DAC+2


fout.close()

print("Time to finish : {} s".format(time.time()-start_time))