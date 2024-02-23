import struct
import os
import sys

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

def clearScreen(isgitbash):
    os.system("") #needed to enable ansi codes. also removes flicker for git bash clear
    if isgitbash:
        os.system("clear") #less flicker than cls
    else:
        #os.system("cls")
        print("\x1b[2J")
        print("\x1b[H")

def listToString(list):
    returnstring = ""
    for entry in list:
        returnstring = returnstring + str(entry)
    return returnstring