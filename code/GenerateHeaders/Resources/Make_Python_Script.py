import os


sample = open("boneTwist.h")
sampleLinesTmp = sample.readlines();
sample.close();
sampleLines = [];

for line in sampleLinesTmp:
    tmp = "";
    for i in range(0, len(line) - 1):
        tmp = tmp + line[i];
    sampleLines.append(tmp);

f = open("Generate_Headers_Bone.py", "w+", newline="\n");

for line in sampleLines:
    f.write("f.write('" + line + "\\n')\n");

f.close();