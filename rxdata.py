from unetpy import UnetSocket
from unetpy import *

s = UnetSocket('192.168.0.11', 1100)
rx = s.receive()                                                
# print(rx.data)
print('from node', rx.from_, ':', bytearray(rx.data).decode())  
s.close()


# s = UnetSocket('192.168.0.11', 1101)
# modem = s.getGateway()
# rx = s.receive()                                                
# print('rx', rx)
# print('from node', rx.from_, ':', bytearray(rx.data).decode())  
# s.close()

# # modem = s.getGateway()                               
# # rx = modem.receive(RxFrameNtf, 5000)                                                
# # print('rx', RxFrameNtf)  
# # s.close()