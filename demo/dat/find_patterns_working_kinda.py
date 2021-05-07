import binascii
import struct

f = open("anisoFrax_80.bgeo", 'rb');
byteLen = 4;

byteList = [];
f.read(3);
byte = f.read(byteLen);

while byte:
    
    if len(byte) < byteLen:
        print(len(byte));
        break;
    [tmp] = struct.unpack('f', byte)
    #tmp = int.from_bytes(byte, byteorder="big", signed=True);
    byteList.append(tmp);
    byte = f.read(byteLen);

f.close();
print(len(byteList));

f = open("test.txt", "w+", newline="\n");
for x in range(0, len(byteList)):
    f.write(str(byteList[x]));
    f.write("\n");
f.close();
