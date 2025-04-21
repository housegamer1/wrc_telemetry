import struct
import json
import os
import datetime
import time

def _resolveFloat(asBytes, precision=2):
    return round(struct.unpack("f", asBytes)[0], precision)

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

def resolveFloatValue(byteValues, round=2):
    asBytes = bytes(byteValues)
    asRpm = _resolveFloat(asBytes, round)
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

loadedIds = None
def resolveId(id, section, shorten=False):
    #print("Resolve id: " + str(id) + ", in section: " + str(section))
    global loadedIds    
    returnString = "N/A"

    if loadedIds == None:
        homeDir = os.path.expanduser('~')
        idFileLocation = homeDir + '/Documents/My Games/WRC/telemetry/readme/ids.json'
        
        if homeDir != None and homeDir != "" and os.path.isfile(idFileLocation):
            idFile = open(idFileLocation, encoding="utf-16")
            #print("id file:" +str(idFile))
            if idFile != None:
                loadedIds = json.load(idFile)
            idFile.close()
        else:
            #print("Unable to open id file")
            pass

    if loadedIds != None:
        for entry in loadedIds[section]:
            if id == entry["id"]:
                returnString = entry["name"]
                break

    if section == "vehicles":
        if id == 124 or id == 125 or id == 124:
            returnString = returnString + " 24" #EA didnt update the names of the vehicles, only the ID
        elif id == 103 or id == 104 or id == 105:
            returnString = returnString + " 23"   

    if section == "vehicle_classes" and shorten:
        returnString = shortenClass(returnString)
    return returnString

def shortenClass(carclass):
    #i dont know what the game exports in other languages here, since my game is in german, some names are annoyingly long.
    #a few of these will work independent of language though.
    #might as well use this to translate german classes into english for the viewers. english names are often shorter too.
    #
    #this function is only intended for displaypurposes, the timesdatabase will contain unaltered class names.

    if carclass ==  "Gruppe B (Heckantrieb)":
        return "Group B RWD"
    elif carclass == "Gruppe B (Allrad)":
        return "Group B 4WD"
    elif carclass == "F2 Bausatzwagen":
        return "F2 Kit Car"
    elif carclass == "Gruppe A":
        return "Group A"
    elif carclass == "World Rally Car 1997-2011":
        return "WRC 97-11"
    elif carclass == "World Rally Car 2017–2021":
        return "WRC 17-21"
    elif carclass == "World Rally Car 2012 - 2016": #funny they put spaces for this one
        return "WRC-12-16"

    else:
        return carclass.replace("(", "").replace(")", "")

def cleanGamemode(gamemode):
    return gamemode.replace("_", " ").title() #capitalizes every words first letter

def roundToNearest(value, nearest):
    return nearest * round(value / nearest)

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))



def pretty_print_time(seconds):
    #shameless inefficient yoink from my telegram bot, cba looking up a smart solution
    playerTimeAsDelta =  str(datetime.timedelta(seconds=seconds))
    if '.' in playerTimeAsDelta:
        playerTimeAsDelta = playerTimeAsDelta[:-4]
    else:
        playerTimeAsDelta = playerTimeAsDelta + ".00"

    playerTimeString = ""

    #fuck this imma format this manually
    while  playerTimeAsDelta.startswith("0"):
        if playerTimeAsDelta.startswith("0:"):
            playerTimeAsDelta = playerTimeAsDelta[2:]
        else:
            playerTimeAsDelta = playerTimeAsDelta[1:]

    if seconds >= 3600:
        playerTimeString = playerTimeAsDelta + " hours"
    elif seconds >= 60:
        playerTimeString = playerTimeAsDelta + " minutes"
    else:
        playerTimeString = playerTimeAsDelta + " seconds"

    return playerTimeString


def parse_stringarray_of_floats(floatarray_in_stringform):
    floatarray_in_stringform = str(floatarray_in_stringform).replace("[", "").replace("]", "").replace(" ", "")
    stringarray = floatarray_in_stringform.split(",")

    floatarray = []

    for entry in stringarray:
        if entry != "":
            floatarray.append(float(entry))

    return floatarray