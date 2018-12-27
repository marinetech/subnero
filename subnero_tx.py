# Settings
ip_address = "192.168.0.11"
number_of_loops = 2
sleep_between_loops = 0
signal_file = 'subnero.sig'

##--------------------------------------##

import sys
import time
import numpy as np
import arlpy as ap
from unetpy import *

# Open connection to the modem
print("-I- connecting to modem: " + ip_address)
try:
    modem = UnetGateway(ip_address, 1100)
except:
    exit(1)

# Load the signal to transmit
print("-I- loading signal from: " + signal_file)
try:
    # signal = np.genfromtxt(signal_file)
    signal = np.loadtxt(signal_file)
except:
    print("-E- failed to load signal file")
    exit(1)

# and transmit the signal...
bb = modem.agentForService(Services.BASEBAND)
for i in range(0,number_of_loops):
    print("-I- Tx #" + str(i+1))
    bb << org_arl_unet_bb.TxBasebandSignalReq(signal=signal.tolist(), fc=0, fs=192000)

    # Verify successfull transmission
    txntf = modem.receive(TxFrameNtf, 5000)
    if txntf is not None: # if successfull
        txtime = txntf.txTime # Extract the transmission start time
        print('-I- Tx started at ' + str(txtime))
    else:
        print('-E- Tx was not successfull')


    if sleep_between_loops:
        print("-I- sleeping for {} seconds".format(sleep_between_loops))
        time.sleep(sleep_between_loops)

modem.close()
