"""
command codes for RFID reader/writter
"""

commands = {}

"""
getHardwareInfo

Header:      AA
Type:        00
Command:     03
PL (MSB):    00    (more significant bit)
PL (LSB):    01    (less significant bit)
Parameter:   00
Checksum:    04
End:         DD
"""
commands["getHardwareInfo"] = "AA000300010004DD"

"""
singleRead

Header:      AA
Type:        00
Command:     22
PL (MSB):    00    (more significant bit)
PL (LSB):    00    (less significant bit)
Checksum:    22
End:         DD
"""
commands["singleRead"] = "AA0022000022DD"

