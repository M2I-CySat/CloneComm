import ax25_function as ax

def appendData(inputBytearray, type, value, intbytecount = 1):
    match type:
        case "int":
            inputBytearray.extend(value.to_bytes(intbytecount, "big"))
        case "str":
            inputBytearray.extend(map(ord, value))
        case "hex":
            inputBytearray.extend(bytearray.fromhex(value))

def makeCySatPacket(subsystem, command, data, dozeros, doaas, doax, srcCall = "KB0MGQ", destCall = "W0ISU "):
    packetlength = 20

    tempdata = bytearray()

    for a in data:
        appendData(tempdata, a[0], a[1])

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
    byte = sum & 0xFF
    print("byte: "+str(byte))
    checksum = 0xFF - byte
    fullcommand.extend(checksum.to_bytes(1, 'big'))
        # //subtract from 0xFF
        # return 0xFF - byte;



    if len(fullcommand) < packetlength and doaas == "true":
        for i in range (0, packetlength - len(fullcommand)):
            fullcommand.extend(bytearray.fromhex("AA"))

    ax.display_bytearray_as_hex(fullcommand)
    if doax == "true":
        finalpacket = ax.makeAx25(srcCall, destCall, fullcommand, 'bytearray', dozeros)
    else:
        finalpacket = fullcommand
    f = open("Newly_Generated_CySat_Packet_For_Uplink.bin", "wb")
    f.write(finalpacket)

# int, str, hex, then value, then byte count if int

<<<<<<< Updated upstream
makeCySatPacket("OBC","01",[])


#makeCySatPacket("ADCS", "0d", [["int", 64, 2], ["str", "Hello"]])
=======
makeCySatPacket("OBC","01",[], "true", "true", "true")


#makeCySatPacket("SDR", "1B", [["hex", "00"]], "false", "false", "false")
#makeCySatPacket("SDR", "01",[], "false", "false", "false")
>>>>>>> Stashed changes
