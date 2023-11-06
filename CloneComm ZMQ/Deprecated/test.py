import binascii
import struct
import array
x = binascii.unhexlify('b62e000052e366667a66408d')
y = array.array('h', x)  
y.byteswap()
s = struct.Struct('<Id')
print(s.unpack_from(y))

# (46638, 943.2999999994321)