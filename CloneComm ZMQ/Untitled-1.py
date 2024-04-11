def convert_to_bytes(num, size):
    data = bytearray()
    if num<0:
        num += (pow(2,8*size))
    for index in range(size-1, -1, -1):
        data.append((int(num) >> (index*8)) & 0xFF)
    return data

def display_bytearray_as_hex(thestring):
    fullstring = ""
    for i in range(0, len(thestring)):
        if (len(str(hex(thestring[i])[2:]))) == 1:
            fullstring = fullstring+"0"
        fullstring = fullstring+hex(thestring[i])[2:]
        fullstring = fullstring+(" ")
    print(fullstring)

data = bytearray()
size = convert_to_bytes(44948, 3)
data.extend(size)
display_bytearray_as_hex(data)
