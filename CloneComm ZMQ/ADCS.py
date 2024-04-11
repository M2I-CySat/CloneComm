import CSPP_generator as CSPP
import struct
import array
import binascii
import time
import requests

def double_to_hex(f):
    return hex(struct.unpack('>Q', struct.pack('<d', f))[0])

def endian_swap_double(invar):
    outvar = ["0"]*18
    outvar[0:1] = invar[0:1]
    outvar[4:5] = invar[14:15]
    outvar[6:7] = invar[12:13]
    outvar[8:9] = invar[10:11]
    outvar[10:11] = invar[8:9]
    outvar[12:13] = invar[6:7]
    outvar[14:15] = invar[4:5]
    outvar[16:17] = invar[2:3]


    return outvar

def TC(num,data):
    data = data.replace(" ","")
    length=round(len(data)/2)+1
    print("Data is "+str(length)+" long")
    datanew = num+data
    print(datanew)

    return CSPP.makeCySatPacket("ADCS","01",[["int",length,1],["hex",datanew,length]], True, True, True)

def TLM(num,out_byte):
    return CSPP.makeCySatPacket("ADCS","03",[["int",num,1],["int",out_byte,1]], True, True, True)

def TC_2():
    unixTimestamp = int(round(time.time()))
    print("Timestamp "+str(unixTimestamp))
    return  CSPP.makeCySatPacket("ADCS","05",[["int",unixTimestamp,4],["int",0,2]], True, True, True)



def TC_45():

    response = requests.get("https://tle.ivanstanojevic.me/api/tle/25544")
    #text = "{\"@context\":\"https:\/\/www.w3.org\/ns\/hydra\/context.jsonld\",\"@id\":\"https:\/\/tle.ivanstanojevic.me\/api\/tle\/25544\",\"@type\":\"Tle\",\"satelliteId\":25544,\"name\":\"ISS (ZARYA)\",\"date\":\"2023-10-16T04:13:26+00:00\",\"line1\":\"1 25544U 98067A   23289.17600325  .00022066  00000+0  38962-3 0  9994\",\"line2\":\"2 25544  51.6421  89.2403 0004841 108.6565  62.5649 15.50277152420558\"}"
    #print("Status Code: "+str(response.status_code))

    text = response.text

    print("Response Contents:")
    print(text)

    array1 = text.split(",")

    for item in array1:
        print("Item: "+str(item))

    values = array1[6].split()+array1[7].split()

    for item in values:
        print("Value: "+str(item))






    Inclination = double_to_hex(float(values[11]))
    Eccentricity = double_to_hex(float("0."+values[13]))
    RAAN = double_to_hex(float(values[12]))
    AOP = double_to_hex(float(values[14]))



    bstarexp = float(values[6][-2:])
    bstarbase = float("0."+values[6][:5])
    bstar = bstarbase*(10**bstarexp)
    bstar = double_to_hex(bstar)
    meanmotion = double_to_hex(float(values[16][:-2]))
    meananomaly = double_to_hex(float(values[15]))
    Epoch = double_to_hex(float(values[3]))

    output = bytearray()

    output.extend(bytearray.fromhex(Inclination[2:]))
    output.extend(bytearray.fromhex(Eccentricity[2:]))
    output.extend(bytearray.fromhex(RAAN[2:]))
    output.extend(bytearray.fromhex(AOP[2:]))
    output.extend(bytearray.fromhex(bstar[2:]))
    output.extend(bytearray.fromhex(meanmotion[2:]))
    output.extend(bytearray.fromhex(meananomaly[2:]))
    output.extend(bytearray.fromhex(Epoch[2:]))



    CSPP.ax.display_bytearray_as_hex(output)

    return CSPP.makeCySatPacket("ADCS","07",[["bytearray", output,"blah"]], True, True, True) #TODO: Make command number real number

TC_2()