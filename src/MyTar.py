import os
import sys
from os import read, write


def findingLengthandName(filesToPrint, fileDescryptor):
    for files in filesToPrint:
        openedFile = os.open(files, os.O_RDONLY)
        ibuf = read(openedFile, 10)
        bytesRead = len(ibuf)
        while len(ibuf):
            ibuf = read(openedFile, 10)
            bytesRead += len(ibuf)
        os.write(fileDescryptor,(files + "," + str(bytesRead) + ",").encode())
        os.close(openedFile)


def tarFileMaker(filesToPrint, fd):
    for files in filesToPrint:
        openedFile = os.open(files, os.O_RDONLY)
        ibuf = read(openedFile, 100)
        while len(ibuf):
            os.write(fd, ibuf)
            ibuf = read(openedFile, 100)
        os.close(openedFile)


def getNamesAndSizes(fileDescryptor):
    tempStr = str(os.read(os.open(fileDescryptor,os.O_RDONLY),1000))
    if tempStr.find("b'") != -1:
        tempStr = tempStr[tempStr.find("b'") + 2:]
    return tempStr.split(",")


def intializeFolder():
    path = os.getcwd() + "/tar"
    if not os.path.exists(path):
        os.makedirs(path)


def getFileNames(fileDescryptor, numOfBytes):
    name = read(fileDescryptor, numOfBytes)
    return name.decode()


def tarExtract(fd, bytesToRead):
    count = 0
    while count < len(bytesToRead):
        ls = os.read(fd, bytesToRead[count])
        count += 1


def createTarFile(fileName):
    path = os.path.join(os.getcwd() + "/tar", fileName)
    if os.path.isfile(path):
        os.remove(path)
        os.mknod(path)
    else:
        os.mknod(path)  # summary to stderr
    return path


def extractFile(bytesAndNames,fd):
    count = 0
    while count < len(bytesAndNames) - 1:
        tempFile = os.open(createTarFile(bytesAndNames[count]),os.O_RDWR)
        count +=1
        fileContents = os.read(fd, int(bytesAndNames[count]))
        os.write(tempFile, fileContents)
        count += 1


def createCompressed():
    compressed = os.open(createTarFile("compressed.txt"), os.O_RDWR)
    tarFileMaker(filesToPrint, compressed)
    os.close(compressed)


def createBytesAndNames():
    bytesAndNames = os.open(createTarFile("bytesAndNames.txt"), os.O_RDWR)
    findingLengthandName(filesToPrint, bytesAndNames)
    os.close(bytesAndNames)

filesToPrint = sys.argv[1:]
ifd = filesToPrint[0]
compressedFile = os.path.join(os.getcwd() + "/tar", "compressed.txt")
bytesNames = os.path.join(os.getcwd() + "/tar", "bytesAndNames.txt")

if filesToPrint[0] == "c" or filesToPrint[0] == "C":
    intializeFolder()
    filesToPrint = filesToPrint[1:]
    createBytesAndNames()
    createCompressed()
elif filesToPrint[0] == "x" or filesToPrint[0] == "X":
    filesToPrint = filesToPrint[1:]
    listofNamesAndBytes = getNamesAndSizes(bytesNames)
    extractFile(listofNamesAndBytes, os.open(compressedFile,os.O_RDWR))
else:
    os.write(1, "ERROR MODE NOT RECOGNIZED".encode())

