"""
Convert a string hex byte values into a byte string. The Hex Byte values may
or may not be space separated.
eg: "AABB0011" to b"AABB0011"
"""
def HexToByte(hexStr):
    return bytes.fromhex(hexStr)

"""
Convert a byte string to it's hex string representation e.g. for output.
"""
def ByteToHex( bins ):
    return ''.join( [ "%02X" % x for x in bins ] ).strip()
