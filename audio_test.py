# Settings
ip_address = "localhost"
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

# Open connection to the modem
print("-I- connecting to modem: " + ip_address)
try:
    sock = UnetSocket('localhost', 1100)
    modem = sock.getGateway()
except:
    print("-I- cannot connect to modem")
    exit(1)

# Load the signal to transmit
print("-I- loading signal from: " + signal_file)
try:
    # signal = np.genfromtxt(signal_file)
    signal = np.loadtxt(signal_file)
    print("-I- signal loaded")
except:
    print("-E- failed to load signal file")
    exit(1)

# Generate a passband 100 ms 12 kHz pulse at a sampling rate of 96 kSa/s:
fs = 12000

bb = modem.agentForService(Services.BASEBAND)
bb << TxBasebandSignalReq(signal=signal, fc=0, fs=fs)