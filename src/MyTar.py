

import os
import sys
from os import read, write

filesToPrint = sys.argv[1:]
ifd = filesToPrint[0]

temp = os.open(ifd, os.O_RDWR)
ibuf = read(temp, 100)
while len(ibuf):
    sbuf = ibuf.decode()
    ibuf = read(temp, 100)
os.write(temp, "AWOOGA".encode())
# summary to stderr

os.close(temp)
print(filesToPrint)
