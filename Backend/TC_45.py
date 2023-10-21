import CSPP_generator as CSPP
import struct

import requests

#response = requests.get("https://tle.ivanstanojevic.me/api/tle/25544")
text = "{\"@context\":\"https:\/\/www.w3.org\/ns\/hydra\/context.jsonld\",\"@id\":\"https:\/\/tle.ivanstanojevic.me\/api\/tle\/25544\",\"@type\":\"Tle\",\"satelliteId\":25544,\"name\":\"ISS (ZARYA)\",\"date\":\"2023-10-16T04:13:26+00:00\",\"line1\":\"1 25544U 98067A   23289.17600325  .00022066  00000+0  38962-3 0  9994\",\"line2\":\"2 25544  51.6421  89.2403 0004841 108.6565  62.5649 15.50277152420558\"}"
#print("Status Code: "+str(response.status_code))

#text = response.text

print("Response Contents:")
print(text)

array = text.split(",")

for item in array:
    print("Item: "+str(item))

values = array[6].split()+array[7].split()

for item in values:
    print("Value: "+str(item))


# Epoch = 
Inclination = values[11]
Eccentricity = values[13]
RAAN = values[12]
AOP = values[14]
bstar = values[6]
meanmotion = values[16]
meananomaly = values[15]
Epoch = values[3]

Inclination = bytearray(struct.pack("f", float(Inclination)))  

CSPP.ax.display_bytearray_as_hex(Inclination)






