
from "/home/daq/BiasScan/ETLSBSF/acquisition_wrapper_DACscan" import * 

run_number=-1

def doRun(nevents,max_time):
	# Take a scan 
	# nevents = total number of events
	# max_time = maximum time before timeout
	ScopeAcquisition(run_number, nevents, max_time)

	# come back to this later
	#os.system(AgilentScopeCommand)
	return 







# Do a one event run for 1 second

# If you have an event 
# DO a second run for more events
# Get the rate 

min_DAC = 200
max_DAC = min_DAC+1

for DAC in range(min_DAC,max_DAC):

	ScopeAcquisition(run_number, 1, 1)
	# Do a one event run for 1 second

	#found_events = doTestRun()

	#if found_events:
	#	doRealRun()