import serial
import sys
import time

from commandCode import commands
from utils import HexToByte

defaultPortID = "usb-1a86_USB2.0-Serial-if00-port0"

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
	# port='/dev/ttyUSB0',
    port = "/dev/serial/by-id/" + defaultPortID,
	baudrate=115200,
	# parity=serial.PARITY_ODD,
	# stopbits=serial.STOPBITS_TWO,
	# bytesize=serial.SEVENBITS
)

cmd = HexToByte(commands["singleRead"])
if not ser.isOpen():
    ser.open()

if ser.isOpen():
    # ongoing = True
    try:
        hexByteArray = []
        # while ongoing :
        ser.write(cmd)
        time.sleep(1) # 1s wait for cmd process and response
        
        while ser.inWaiting() > 0:
            hexByteArray.append(ser.read(1))
            
        if len(hexByteArray) != 0:
            data = [h.decode() for h in [hb.hex() for hb in hexByteArray]]
            print(">>", data)
        else:
            print("no response")
            # ongoing = False
    finally:
        ser.close()