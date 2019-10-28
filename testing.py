"""
Convert a string hex byte values into a byte string. The Hex Byte values may
or may not be space separated.
"""
def HexToByte(hexStr):
    return bytes.fromhex(hexStr)

b = HexToByte("AA001122DD")

print(type(b))
print(b)

"""
Convert a byte string to it's hex string representation e.g. for output.
"""
def ByteToHex( bins ):
    return ''.join( [ "%02X" % x for x in bins ] ).strip()

h = ByteToHex(b)

print(type(h))
print(h)