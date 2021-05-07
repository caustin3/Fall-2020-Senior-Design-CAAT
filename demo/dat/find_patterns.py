import binascii
import struct

f = open("anisoFrax_80.bgeo", 'rb');
byteLen = 4;

floatList = [];
f.read(3);
byte = f.read(byteLen);
counter = 0;
while byte:
    
    if len(byte) < byteLen:
        print(len(byte));
        break;
    [tmp] = struct.unpack('f', byte)
    #tmp = int.from_bytes(byte, byteorder="big", signed=True);
    floatList.append(byte);
    byte = f.read(byteLen);
    

f.close();

f = open("test.txt", "w+", newline="\n");
for x in range(0, len(byteList)):
    f.write(str(byteList[x]));
    f.write("\n");
f.close();
