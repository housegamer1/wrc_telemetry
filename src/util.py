import struct
import os


def _resolveFloat(asBytes):
    return round(struct.unpack("f", asBytes)[0], 2)

def _resolveDouble(asBytes):
    return round(struct.unpack("d", asBytes)[0], 2)

def _resolveInt(asBytes):
    return int.from_bytes(asBytes, byteorder="little")

def _mpsToKmh(mps):
    return round(mps * 3.6, 2)

def mToKm(m):
    return round(m / 1000, 2)

def resolveSpeed(byteValues):
    asBytes = bytes(byteValues)
    asMps =  _resolveFloat(asBytes) # in m/s
    asKmh = _mpsToKmh(asMps)
    return asKmh

def resolveSpeedRound(byteValues):
    return round(resolveSpeed(byteValues))

def resolveIntValue(byteValues):
    asBytes = bytes(byteValues)
    asInt = _resolveInt(asBytes)
    return asInt

def resolveFloatValue(byteValues):
    asBytes = bytes(byteValues)
    asRpm = _resolveFloat(asBytes)
    return asRpm
    
def resolveFloatValueRound(byteValues):
    return round(resolveFloatValue(byteValues))

def resolveDoubleValue(byteValues):
    asBytes = bytes(byteValues)
    asRpm = _resolveDouble(asBytes)
    return round(asRpm)

def resolveDoubleValueRound(byteValues):
    return round(resolveDoubleValue(byteValues))

def resolveBoolean(byteValues):
    return bool(byteValues[0])

def listToString(list, newline):
    returnstring = ""
    for entry in list:
        returnstring = returnstring + str(entry)
        if newline:
            returnstring = returnstring + "\n"

    return returnstring

def setcolor(color):
    if color == "white":
        return "\x1b[0m"
    elif color == "red":
        return "\x1b[1;31;40m"
    elif color == "green":
        return "\x1b[1;32;40m"
    elif color == "yellow":
        return "\x1b[1;33;40m"
    elif color == "blue":
        return "\x1b[1;34;40m"
    elif color == "purple":
        return "\x1b[1;35;40m"
    
def quit(args):
        print("")

        if args.isgitbash:
            print('\033[?25h', end="") #bring cursor back

        print("Quitting")
        exit(0)


def drawSideBySide(leftDraw, rightDraw):
    returnstring = ""    
    leftLines = leftDraw.split("\n")
    rightLines = rightDraw.split("\n")

    lenL = len(leftLines)
    lenR = len(rightLines)

    counter = 0

    if lenL >= lenR:
        #loop over left, draw left then right
        for lLine in leftLines:
            returnstring = returnstring + lLine
            
            if counter < len(rightLines):
                returnstring = returnstring + "\t" + rightLines[counter]

            counter = counter +1
            returnstring = returnstring + "\n"

    else:
        #loop over right, draw left then right
        for rLine in rightLines:
            if counter < len(leftLines):
                returnstring = returnstring + leftLines[counter]

            returnstring = returnstring + "\t" + rLine
            counter = counter +1
            returnstring = returnstring + "\n"

    return returnstring