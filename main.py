import sys
import time

from commandCode import commands
from utils import HexToByte

from barcode import readBarcode

print("start\n")
print("result %s" % readBarcode())
print("end\n")