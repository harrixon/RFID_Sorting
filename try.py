hba = [
    'aa', # header
    '02', # type
    '22', # cmd
    '00', # antena id
    '11', # 指令参数长度 PL (LSB)
    'c9', # RSSI, 芯片输入端信号强度, unit: dBm
    '30', '00', 'e2', '00', '00', '1b', '85', 
    '03', '01', '63', '19', '20', '8f', '61', '83', '67', '2a', 'dd', 'aa', '02', '22', '00', '11', 'd1', 
    '34', '00', # PC (MSB, LSB), Protocol Control
    '30', '08', '33', 'b2', 'dd', 'd9', # EPC (MSB)
    '01', '40', '00', '00', '00', '00', # EPC (LSB)
    'c4', '1e', # CRC (MSB, LSB): Cyclic Redundancy Check, used by the reader to verify whether the received EPC is correct or not, as a verification of the wireless link between the tag and the reader.
    '30', # checksum
    'dd'  # end byte
]

sa = [b.hex() for b in hba[-6:-4]]

h = "".join(sa)

b = bytes.fromhex(h)

print(b.decode('utf-8'))

# print(type(hb)) # bytes

# b = hb.hex()
# print(type(b))  # str
# print(b)        # aa



# # s = b.decode()
# # print(s)