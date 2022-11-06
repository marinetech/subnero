# Settings
ip_address = "192.168.0.11"
rx_out_folder = "rx_out"
rx_out_file = "rx_rec_"
number_of_rec = 5

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


bb = modem.agentForService(Services.BASEBAND)

file_idx = 0
for i in range(0,number_of_rec):
    print("-I- rx #" + str(i+1))

    # what is the next avaiable file name?    
    next_out_file = None
    while not next_out_file:
        possible_name = "{}/{}{}".format(rx_out_folder, rx_out_file, file_idx)
        if os.path.isfile(possible_name): # already in use?
            file_idx = file_idx + 1
        else:
            next_out_file = possible_name

    # Record a baseband signal
    bb << RecordBasebandSignalReq(recLen=24000)

    # Receive the notification when the signal is recorded
    rxntf = modem.receive(RxBasebandSignalNtf, 192000)
    if rxntf is not None:
        # Extract the recorded signal
        rec_signal = rxntf.signal
        # rec_signal.tofile(next_out_file)
        np.savetxt(next_out_file, rec_signal)
        print('-I- signal was recorded successfully')
    else:
        print('-E- signal was not recorded successfully')

modem.close()
