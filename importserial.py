from re import X
import serial
import serial.tools.list_ports as port_list

ports = list(port_list.comports())
for p in ports:
    print (p)

""" ser = serial.Serial('/dev/ttyS0')  # open serial port

print(ser.name)         # check which port was really used

ser.write(b"urmom")
x=ser.read()
line = ser.readline()
print(X)

ser.close() """