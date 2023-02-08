

import os
import sys
from os import read, write

filesToPrint = sys.argv[1:]
print(len(filesToPrint))
ifd = filesToPrint[0]

temp = os.open(ifd, os.O_RDWR)
ibuf = read(temp, 100)
while len(ibuf):
    sbuf = ibuf.decode()
    if sbuf.find("/x") != -1:
        print(sbuf)
        print("found /x")
    print(sbuf)
    ibuf = read(temp, 100)
os.write(temp, "/x".encode())
# summary to stderr

os.close(temp)
print(filesToPrint)
