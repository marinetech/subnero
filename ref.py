from unetpy import *

modem = UnetGateway('192.168.0.11')
phy = modem.agentForService(Services.PHYSICAL)
print(phy[0][0])
