import crcmod
import crcmod.predefined
import sys
# This program is designed to generate AX.25 packets for transmission to CYSAT-1.
# With blood, sweat, and tears, by Steven Scheuermann
# With assistance from Henry Shires, Vanessa Whitehead, and Manas Mathur

# The main function, makeAx25(), takes in a payload and outputs a bytearray containing the Endurosat packet which contains that payload.
# There are a few other helper functions related to weird bit/byte conversions I had to do because Python doesn't have built in functions for that




# For CySat, Ground station is KB0MGQ, satellite is W0ISU. Make sure to add spaces to bring this up to six characters.
srcCall = "KB0MGQ"
destCall = "W0ISU "
# The contents of the AX.25 packet. This will eventually be a function argument when this is made into a function.
informationField = "Why is this so difficult"

sys.set_int_max_str_digits(100000)

# Takes a string of bits ("0101010") and converts it to a bytes object
def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])

# Takes a string of bits ("0101000110") and converts it to a bytearray, but left justified
def bitstring_to_bytes_but_left_justified(bits):
    bytes = [bits[i:i+8] for i in range(0, len(bits), 8)]
    exitstring = ""
    for i in range(len(bytes)):
        # This is somehow uglier than my face, I didn't know that was possible
        exitstring = exitstring + \
            (hex(int(bytes[i].ljust(8, "0"), 2))[2:].zfill(2))
    # print(exitstring)
    return (bytearray.fromhex(exitstring))

# Prints a string ("Hello World") as hex for debug purposes
def display_string_as_hex(thestring):
    fullstring = ""
    for i in range(0, len(thestring)-1):
        # fullstring=fullstring+("0x")
        fullstring = fullstring+("{0:02x}".format(ord(thestring[i])))
        fullstring = fullstring+(" ")
    print(fullstring)

# Prints a bytearray as hex for debug purposes
def display_bytearray_as_hex(thestring):
    fullstring = ""
    for i in range(0, len(thestring)):
        if (len(str(hex(thestring[i])[2:]))) == 1:
            fullstring = fullstring+"0"
        fullstring = fullstring+hex(thestring[i])[2:]
        fullstring = fullstring+(" ")
    print(fullstring)

# Prints a bytearray as hex with no spaces for debug purposes
def display_bytearray_as_hex_no_spaces(thestring):
    fullstring = ""
    for i in range(0, len(thestring)):
        if (len(str(hex(thestring[i])[2:]))) == 1:
            fullstring = fullstring+"0"
        fullstring = fullstring+hex(thestring[i])[2:]
        # fullstring=fullstring+(" ")
    print(fullstring)

# Converts a bytearray into hex
def return_bytearray_as_hex(thestring):
    fullstring = ""
    for i in range(0, len(thestring)):
        if (len(str(hex(thestring[i])[2:]))) == 1:
            fullstring = fullstring+"0"
        fullstring = fullstring+hex(thestring[i])[2:]
        # fullstring=fullstring+(" ")
    return (fullstring)

# Converts a bytearray into hex with spaces
def return_bytearray_as_hex_spaces(thestring):
    fullstring = ""
    for i in range(0, len(thestring)):
        if (len(str(hex(thestring[i])[2:]))) == 1:
            fullstring = fullstring+"0"
        fullstring = fullstring+hex(thestring[i])[2:]
        fullstring=fullstring+(" ")
    return (fullstring)

"""
Makes an Ax.25 packet
Parameters:
    :param srcCall - Six character all caps string - radio callsign for the groundstation (Ex: "KB0MGQ") (Ensure that there are six characters, add spaces if your callsigns are shorter than 6 characters)
    :param destCall - Six character all caps string - radio callsign for the satellite (Ex: "W0ISU ") (Ensure that there are six characters, add spaces if your callsigns are shorter than 6 characters)
    :param informationField - ascii string or bytearray depending on ecoding - the payload of the Ax.25 packet. Can be an ascii string (Ex: "Hello World") or a bytearray (Ex: make a bytearray and extend it as needed, can do non ascii characters")
    :param encoding - string - 'ascii' or 'bytearray', determines the format of informationField
    :param dozeros - boolean - whether or not the output should be prepended and postpended by a lot of zeros. It should help improve packet detection if the radios on either end have a tendency to cut off the start and end of transmissions.
Returns:
    A bytearray containing the Ax.25
"""

def makeAx25(srcCall, destCall, informationField, encoding, dozeros):

    # Callsigns

    axlayer = bytearray()

    # Destination Address

    # Convert the destination callsign to bits
    destBits = ''.join(format(ord(x), '08b') for x in destCall) # Why isn't there a better Python function to convert to bits

    # Leftshift the bits because the format requires it
    destBitsLshift = (int(destBits, 2) << 1)

    # Reformat
    destBitsLshift2 = "{0:b}".format(destBitsLshift)

    # Append to axlayer
    axlayer.extend(bitstring_to_bytes(destBitsLshift2))

    # Append first SSID to axlayer
    SSID = bytearray.fromhex("E0")
    axlayer.extend(SSID)

    # Source Address - Repeat everything all over again

    srcBits = ''.join(format(ord(x), '08b') for x in srcCall)
    srcBitsLshift = (int(srcBits, 2) << 1)
    srcBitsLshift2 = "{0:b}".format(srcBitsLshift)
    axlayer.extend(bitstring_to_bytes(srcBitsLshift2))

    # SSID
    # SSID is E1 instead of E0 for this one, I think the 1 at the end is the 1 we were bitshifting everything left for and the E is a predefined consequence of that.
    axlayer.extend(bytearray.fromhex("E1"))

    # Control
    axlayer.extend(bytearray.fromhex("03"))  # Predefined byte

    # PID
    axlayer.extend(bytearray.fromhex("F0"))  # Predefined byte

    # Information Field
    if encoding == 'ascii':
        # Converts ascii input to bytearray if the information field is a string
        informationField_in_hex = bytearray(informationField, 'ascii')
        axlayer.extend(informationField_in_hex)
    elif encoding == 'bytearray':
        # Adds information field to the bytearray if the information field is already a bytearray
        axlayer.extend(informationField)

    # CRC-16

    # The CRC is the CCIT crc, also called the X-25 CRC.
    crc16_function = crcmod.predefined.mkPredefinedCrcFun('x-25')
    crc_value = crc16_function(axlayer)

    # However we need to swap the order of the bytes (this is ugly and I could have done it easier but this works)
    crc_value_full = bytearray.fromhex(
        str(hex(crc_value))[4:6].zfill(2)+str(hex(crc_value))[2:4].zfill(2))
    axlayer.extend(crc_value_full)

    # Yay! The whole Ax.25 part is done now!

    # Next up is the HDLC step. The first thing we need to to is reverse the order of the bits in each byte.

    axstring = return_bytearray_as_hex(axlayer)
    # axbits=''.join(format(ord(x), '08b') for x in axstring)
    axbits = bin(int(axstring, 16))[2:].zfill(8)

    axbytes = [axbits[i:i+8] for i in range(0, len(axbits), 8)]
    reversedbits = ""
    for i in range(0, len(axbytes)):
        reversedbits += axbytes[i][::-1]
    # reversedbytes = [reversedbits[i:i+8] for i in range(0, len(reversedbits), 8)]

    # After reversing the bit order, it is time to do bit stuffing: Adding a 0 after 5 consecutive 1s. This is removed at the other end.
    # Later on characters that have 6 1s in the row serve as control characters saying "Hey! Here's a frame!" so we want to make sure that we never have more than 5 1s in a row so we don't accidentally interfere.

    onescounter = 0
    stuffedbits = ""
    for i in range(0, len(reversedbits)):
        stuffedbits = stuffedbits+reversedbits[i]
        if reversedbits[i] == "1":
            onescounter = onescounter+1
        else:
            onescounter = 0
        if onescounter == 5:
            stuffedbits = stuffedbits+"0"
            onescounter = 0

    # Append 4 7E bytes at the binary level. We can't just do bytearray.extend() here because we might not have a multiple of 8 bits.
    # Basically we may not have a whole number of bytes, and the standard calls for appending to the last bit instead of adding more bits to make a full byte.

    # We also need to prepend 9 7E bytes

    # These are the preamble, starting flag, ending flag, and postamble

    # 7E = 01111110
    sevenE = "01111110"

    # Try not to scream in terror
    withPreambleAndPostamble = sevenE+sevenE+sevenE+sevenE+sevenE + \
        sevenE+sevenE+sevenE+sevenE+stuffedbits+sevenE+sevenE+sevenE+sevenE

    # I am the pi-rate, master of the seven E's

    # Okay so we were going to do scrambling in GNU Radio but I'm having issues as the GNU scrambled adds 17 bits to the beginning
    # Scrambling is a mathematical process that basically randomizes the data
    # In this case, the current bit is the EXOR of the current bit plus the bits transmitted 12 and 17 bits earlier
    # This scrambling thing self synchronizes somehow so the exact seed doesn't matter
    # I will first try removing the seventeen seed bits, the way the UHF gave it to me, but I might have to add them back in like how GNU Radio does it

    scrambledBits = "00000000000000000"
    # Switching it to this one for maybe better debugging but it didn't work, but its working now so im not gonna touch it
    scrambledBits = "00111010000000000"
    # It can probably be any sequence if I understand it right but I don't want to chance it

    # The whole scrambler
    for i in range(0, len(withPreambleAndPostamble)):
        scrambledBits = scrambledBits+str((int(scrambledBits[i+17-12]) ^ int(
            scrambledBits[i+17-17])) ^ int(withPreambleAndPostamble[i]))

    # Remove the first seventeen "seed" bits
    reduced_scrambledBits = scrambledBits[17:]

    # Convert back to bytes

    # payloadBytes=bitstring_to_bytes_but_left_justified(reduced_scrambledBits)
    # display_bytearray_as_hex_no_spaces(payloadBytes)

    # We might have to remove the very last byte I'm not sure
    # I won't do that for now but I will probably do that later
    # But if we just arbitrarily chop off the last byte then if it was already only 8 long then we chopped off a good byte, make sure to check if it is a whole number of bytes first
    # I prbably don't have to remove it
    # But I might
    # This project I swear

    # NRZI Encoding

    # For HDLC, a zero is encoded as a transition from radio high to radio low or radio low to radio high.
    # A one is encoded as staying at the same state
    # I think we start at low but I'm not sure

    currentstate = "0"  # Start off at low state. A 1 is a high state
    NRZIstring = ""

    for i in range(0, len(reduced_scrambledBits)):
        # Current data is 0 so we should change
        if reduced_scrambledBits[i] == "0":
            if currentstate == "0":
                currentstate = "1"
            elif currentstate == "1":
                currentstate = "0"
        # Current data is 1 so we should not change
        elif reduced_scrambledBits[i] == "1":
            dave = 1  # Gotta fill in something for clarity, I don't need this whole elif but it makes it easier to mentally keep track of
        NRZIstring = NRZIstring+currentstate

    # Convert back to bytes

    Data_Field_2_Bytes = bitstring_to_bytes_but_left_justified(NRZIstring)
    # display_bytearray_as_hex_no_spaces(payloadBytes)

    # This *should* be the proper ax.25 stuff. Now to wrap it in an endurosat packet.

    # Message content (Data Field 2)

    # Header and footer

    overall = bytearray()
    bothdatafields = bytearray()

    # Preamble and Sync Word
    overall.extend(bytearray.fromhex("AAAAAAAAAA7E"))

    # Length of Data Field 2

    Data_Field_2_Bytes_Length = str(hex(len(Data_Field_2_Bytes)))[2:]
    bothdatafields.extend(bytearray.fromhex(Data_Field_2_Bytes_Length))

    # Data Field 2

    bothdatafields.extend(Data_Field_2_Bytes)

    # CRC16

    crc16_function = crcmod.mkCrcFun(
        0x11021, initCrc=0xFFFF, rev=False, xorOut=0x0000)

    crc_value = crc16_function(bothdatafields)

    # Assemble it into one packet called overall

    overall.extend(bothdatafields)

    crc_value_converted = str(hex(crc_value))[2:].zfill(4)
    overall.extend(bytearray.fromhex(crc_value_converted))

    withzeros = bytearray()
    if dozeros == True:
        withzeros.extend(bytearray.fromhex(
            "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"))
        withzeros.extend(overall)
        withzeros.extend(bytearray.fromhex(
            "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"))
    else:
        withzeros.extend(overall)
    # print("CRC value: "+hex(crc_value)[2:].zfill(4))
    #print("Hex bytes: ", end="")
    #display_bytearray_as_hex(withzeros)
    return withzeros


def decode_ax25(in_bytearray):

    # Convert to string for bit operations
    axstring = return_bytearray_as_hex(in_bytearray)
    axbits = bin(int(axstring, 16))[2:].zfill(8)
    #print(axbits)
    prevstate = "0"
    currentstate = "0"  # Start off at low state. A 1 is a high state
    NRZIstring = ""

    for i in range(0, len(axbits)):
        currentstate = axbits[i]
        if currentstate == prevstate:
            # No change, is a 1
            NRZIstring+="1"
        else:
            # Change, is a 0
            NRZIstring = NRZIstring + "0"
        prevstate = currentstate

    # Convert back to bytes

    Data_Field_2_Bytes = bitstring_to_bytes_but_left_justified(NRZIstring)

    # Descrambling

    descrambled = [0] * len(Data_Field_2_Bytes)
    descrambledByte = 0
    lfsr = 0b00000000000000000000000000000000
    arr = bytearray(Data_Field_2_Bytes)
    #start descrambling:
    for i in range(len(descrambled)):
        for j in range(8):
            curbit = (arr[i] >> (7-j)) & 1
            lfsr = ((lfsr << 1) | curbit)
            X12 = (lfsr >> 12) & 1
            X17 = (lfsr >> 17) & 1
            outbit = ((curbit) ^ ((X12 ^ X17))) & 1
            descrambledByte = (descrambledByte << 1) | outbit
        descrambled[i] = descrambledByte
        #print("Byte "+str(i)+" Int "+str(int(descrambledByte))+" Str "+str(descrambledByte))
        descrambledByte = 0
    #print("Done descrambling")
    descrambled = bytearray(descrambled)


    # Strip first 3 non 7E bytes and last bytes except the one that doesn't matter ahhh
    stripped = descrambled[3:]
    while stripped[0] == 0x7E:
        stripped = stripped[1:]
    endhex = stripped[-1]
    while stripped[-1] == endhex:
        stripped = stripped[:-1]

    #display_bytearray_as_hex(stripped)

    # Conver to string again
    stripped = return_bytearray_as_hex(stripped)
    stripped = bin(int(stripped, 16))[2:].zfill(8)
    #print(stripped)
    # De-bit stuff

    onescounter = 0
    destuffedbits = "0" # Should stert with 1 for reasons
    for i in range(0, len(stripped)):
        if stripped[i] == "1":
            onescounter = onescounter+1
        else:
            onescounter = 0
        if onescounter == 5:
            #stuffedbits = stuffedbits+"0"
            onescounter = 0
        else:
            destuffedbits = destuffedbits+stripped[i]
    #destuffedbits = destuffedbits[:128]+destuffedbits[129:]
    #print(destuffedbits)

    # Reverse order of bits in each byte
    axstring = bitstring_to_bytes_but_left_justified(destuffedbits)
    axstring = return_bytearray_as_hex(axstring)
    # axbits=''.join(format(ord(x), '08b') for x in axstring)
    axbits = bin(int(axstring, 16))[2:].zfill(8)

    axbytes = [axbits[i:i+8] for i in range(0, len(axbits), 8)]
    reversedbits = ""
    for i in range(0, len(axbytes)):
        reversedbits += axbytes[i][::-1]

    callsigns = "0"+reversedbits[:112]
    callsigns = bitstring_to_bytes_but_left_justified(callsigns)
    #display_bytearray_as_hex(callsigns)

    
    reversedbits = bitstring_to_bytes_but_left_justified(reversedbits)
    #reversedbits = return_bytearra
    totalstring = bytearray(callsigns[0:6])
    twenty = bytearray.fromhex("20")
    totalstring.extend(twenty)
    totalstring.extend(callsigns[7:13])
    totalstring.extend(twenty)
    totalstring.extend(reversedbits[16:-3])
    #totalstring = callsigns[1:6]+0x20+callsigns[8:13]+0x20+reversedbits[14:]
    totalstring=totalstring.decode("utf-8","replace")

    totalstring = reversedbits.decode("utf-8","replace")
    #print(totalstring)
    #display_bytearray_as_hex(reversedbits)
    return totalstring

#testarray = bytearray.fromhex("FEF16E90A0BCA56AFAFE463584B65A6E788190B50FA3D2399AAB0381E1B08FB4E4FA59BCEF7EE435692242D1540EF0D7CAA8F0")

#decode_ax25(testarray)