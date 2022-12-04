# Settings
ip_address = "192.168.0.12"
number_of_loops = 2
sleep_between_loops = 0
signal_file = 'PortoVeryShort'

##--------------------------------------##

import sys
import time
import numpy as np
import arlpy.signal as asig
import arlpy.plot as plt
from unetpy import *
import matplotlib.pyplot as plt1

# Open connection to the modem
print("-I- connecting to modem: " + ip_address)
try:
    sock = UnetSocket(ip_address, 1100)
    modem = sock.getGateway()
except:
	print("-I- cannot connect to modem")
	exit(1)

count=0

while True:
	################### Transmit and record a signal ##########################
	# Look for agents poviding baseband service
	bb = modem.agentForService(Services.BASEBAND)
	# Load the baseband signal to be transmitted.
	# signal.txt contains the same signal as csig in previous section
	# Format: array with alternate real and imag values
	# tx_signal = np.genfromtxt(signal_file, delimiter=',')
	fs = 96000
	fc=24000

	pb_signal = asig.sweep(20000,32000, 0.5, fs)
	tx_signal=asig.pb2bb(pb_signal,fs,fc,fd=24000,flen=127,cutoff=None)

	# Transmit the baseband signal
	# rxntf = modem.receive(RxBasebandSignalNtf, 5000)
	bb << TxBasebandSignalReq(preamble=3, signal=tx_signal,fc=fc)

	# plt.plot(tx_signal, fs=fs)
	# plt.specgram(tx_signal, fs=fs)

	txntf = modem.receive(TxFrameNtf, 1500)
	if txntf is not None:
	    # Request a recording from txTime onwards for a duration of 2x the original transmitted signal.
	    bb << RecordBasebandSignalReq(recTime=txntf.txTime, recLength=(len(tx_signal)*2))
	else:
	    print('Transmission not successfull, try again!')

	# Read the receive notification
	rxntf = modem.receive(RxBasebandSignalNtf, 1500)
	rxntf.fc
	rxntf.fs

	if rxntf is not None:
	    # Extract the recorded signal
	    rec_signal = rxntf.signal
	    print('Successfully recorded signal after transmission!')
	    # The recorded signal is saved in `rec_signal` variable
	    # It can be processed as required by the user.
	    print("Rec signal:", rec_signal)
	    y = asig.bb2pb(rec_signal, rxntf.fs, rxntf.fc, fs)
	    # plt.plot(y, fs=fs)
	    plt.specgram(y, fs=fs)
	    np.savetxt('rx_signal'+str(count)+'.txt',y)
	    time.sleep(3)
	    count += 1

	else:
	    print('Recording not successfull, try again!')

################### Close connection to modem ################################

modem.close()
