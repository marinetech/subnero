from unetpy import UnetSocket

s = UnetSocket('192.168.0.12', 1100)
s.send('hello!', 0)                              
s.close()