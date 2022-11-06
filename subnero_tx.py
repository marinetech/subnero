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
x = asig.cw(12000, 0.5, fs)

# and transmit it using the baseband service:

bb = modem.agentForService(Services.BASEBAND)
bb << TxBasebandSignalReq(signal=signal, fc=0, fs=fs)
txntf = modem.receive(TxFrameNtf, timeout=2000)

# Now let's ask the modem to record a signal for us:

bb << RecordBasebandSignalReq(recLength=4800) 
rec = modem.receive(RxBasebandSignalNtf, timeout=2000)
rec.fc
rec.fs

print('rec', rec);

# The notification has 4800 baseband (complex) samples as we had asked, and is sampled at a baseband rate of 12 kSa/s. The carrier frequency used by the modem is 12 kHz. 
# We can convert our recorded signal to passband if we like:

y = asig.bb2pb(rec.signal, rec.fs, rec.fc, fs)
plt.plot(y, fs=fs)
plt.specgram(y, fs=fs)

# y = asig.bb2pb(txntf.signal, txntf.fs, txntf.fc, fs)
# plt.plot(y, fs=fs)
# plt.specgram(y, fs=fs)

# and transmit the signal...
# bb = modem.agentForService(Services.BASEBAND)
# for i in range(0,number_of_loops):
#     print("-I- Tx #" + str(i+1))
#     bb << TxBasebandSignalReq(signal=signal.tolist(), fc=0, fs=192000)

#     # Verify successfull transmission
#     txntf = modem.receive(TxFrameNtf, 5000)
#     if txntf is not None: # if successfull
#         txtime = txntf.txTime # Extract the transmission start time
#         print('-I- Tx started at ' + str(txtime))
#     else:
#         print('-E- Tx was not successfull')


#     if sleep_between_loops:
#         print("-I- sleeping for {} seconds".format(sleep_between_loops))
#         time.sleep(sleep_between_loops)

modem.close()
