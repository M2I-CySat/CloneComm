import ax25_function as ax

def appendData(inputBytearray, type, value, intbytecount = 1):
    print("intbytecount "+str(intbytecount))
    match type:
        case "int":
            inputBytearray.extend(value.to_bytes(intbytecount, "little"))
        case "str":
            inputBytearray.extend(map(ord, value))
        case "hex":
            inputBytearray.extend(bytearray.fromhex(value))

def makeCySatPacket(subsystem, command, data, dozeros, doax, replaceZeros, srcCall = "KB0MGQ", destCall = "W0ISU "):
    """
    Generate CySat Packet for transmission.

    :param str subsystem: What subsystem the message is meant for.
    :param str command: Command ID in hex: "0x05"
    :param str data: Data, kinda weird
    :param bool dozeros: Whether or not the message is padded with zeros on either end
    :param bool doax: Whether or not the message is wrapped in an ax.25 packet/Endurosat header (payload uses just CSPP)
    :param replaceZeros: Replaces 0x00 with 5x 0xAA because something in the chain is terminating commands after 0x00.
    :param str srcCall: Source callsign
    :param str destCall: Destination callsign
    """

    tempdata = bytearray()

    for a in data:
        appendData(tempdata, a[0], a[1], a[2])

    dataLength = len(tempdata).to_bytes(1, "big")

    match subsystem:
        case "OBC":
            subhex = "0A"
        case "ADCS":
            subhex = "14"
        case "EPS":
            subhex = "1E"
        case "UHF":
            subhex = "0E"
        case "SDR":
            subhex = "28"
        case "EOL":
            subhex = "5A"

    fullcommand = bytearray()

    fullcommand.extend(bytearray.fromhex("FF"))
    fullcommand.extend(bytearray.fromhex(subhex))
    fullcommand.extend(bytearray.fromhex(command))
    fullcommand.extend(dataLength)
    fullcommand.extend(tempdata)
    

    # Temporary checksum

    # TODO: Proper checksumming
    sum = 0
    for i in fullcommand:
        sum += i
        print("i is "+str(i)+", sum is "+str(sum))
        # //take the lowest 8 bitsvfr5
    sum=sum-0xFF
    byte = sum & 0xFF
    print("byte: "+str(byte))
    checksum = 0xFF - byte
    fullcommand.extend(checksum.to_bytes(1, 'big'))
        # //subtract from 0xFF
        # return 0xFF - byte;

    # Zero replacement - UHF or something doesn't like 0x00s, so they are replacex with 5x 0xAA and re-replaced with 0x00 on the other end
    if replaceZeros:
        fullcommand2 = bytearray()
        for i in range (0, len(fullcommand)):
            if fullcommand[i] == 0x00:
                fullcommand2.extend(bytearray.fromhex("AAAAAAAAAA"))
            else:
                fullcommand2.append(fullcommand[i])
        fullcommand = fullcommand2
    
    ax.display_bytearray_as_hex(fullcommand)
    if doax == True:
        finalpacket = ax.makeAx25(srcCall, destCall, fullcommand, 'bytearray', dozeros)
    else:
        finalpacket = fullcommand
    f = open("Newly_Generated_CySat_Packet_For_Uplink.bin", "wb")
    f.write(finalpacket)

# int, str, hex, then value, then byte count if int

<<<<<<< Updated upstream
makeCySatPacket("OBC","09",[["int", 5, 2]], True, True, True)
=======
# makeCySatPacket("OBC","01",[], True, True, True)
>>>>>>> Stashed changes

makeCySatPacket("SDR","01",[],False,False,False) # Payload Power Request
#makeCySatPacket("SDR","19",[["int",495,2]],False,False,False) # Take Measurement
makeCySatPacket("SDR","1B",[["hex","00",0]],False,False,False) # Transfer File
