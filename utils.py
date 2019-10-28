"""
Convert hex string into bytes
eg: "AABB0011" to b"AABB0011"
"""
def HexToByte(hexStr):
    return bytes.fromhex(hexStr)