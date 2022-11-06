ip_address = "192.168.0.11"
rx_out_folder = "sw_out"
rx_out_file = "sw_rec_"
number_of_loops = 5


##--------------------------------------##

import sys
import os
import time
import numpy as np
import arlpy as ap
from unetpy import *

# Open connection to the modem
print("-I- connecting to modem: " + ip_address)
try:
    sock = UnetSocket('192.168.0.11', 1100)
    modem = sock.getGateway()
except:
    exit(1)

# If necessary, create out folder
if not os.path.exists(rx_out_folder):
    os.makedirs(rx_out_folder)

################### Transmit and record a signal ##########################

bb = modem.agentForService(Services.BASEBAND)
for i in range(0,number_of_loops):
    print("-I- Tx #" + str(i+1))
    bb << TxBasebandSignalReq(signal=signal.tolist(), fc=0, fs=192000)

    txntf4 = modem.receive(TxFrameNtf, 5000)
    if txntf4 is not None:
        # Request a recording from txTime onwards
        bb << RecordBasebandSignalReq(recTime=txntf4.txTime, recLen=(len(tx_signal)*2))
    else:
        print('Transmission not successfull, try again!')

    # Read the receive notification
    rxntf4 = modem.receive(RxBasebandSignalNtf, 5000)

    if rxntf is not None:
        # Extract the recorded signal
        rec_signal = rxntf4.signal
        print('Successfully recorded signal after transmission!')
        # The recorded signal is saved in `rec_signal` variable
        # It can be processed as required by the user.
    else:
        print('Recording not successfull, try again!')




    if sleep_between_loops:
        print("-I- sleeping for {} seconds".format(sleep_between_loops))
        time.sleep(sleep_between_loops)

modem.close()
