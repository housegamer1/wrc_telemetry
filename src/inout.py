import util
import os
import msvcrt
import time
import interpret
import ast
import json
import csv
import datetime

currentScreen = 2
recordingStatus = 0
replayMode = 0
selected = 0
skipAhead = 0
toggleAccelerometer = 0
togglePowerband = 0
def showMenu(args):
    readInput(args)

    menuString = ""
    if currentScreen == 1:
       menuString = menuString + util.setcolor("yellow")
    menuString = menuString + "(1) Dashboard" + util.setcolor("white") + " | "

    if currentScreen == 2:
       menuString = menuString + util.setcolor("yellow")
    menuString = menuString + "(2) Graphs" + util.setcolor("white") + " | "

    if currentScreen == 3:
       menuString = menuString + util.setcolor("yellow")
    menuString = menuString + "(3) Suspension" + util.setcolor("white") + " | "

    if currentScreen == 4:
       menuString = menuString + util.setcolor("yellow")
    menuString = menuString + "(4) Raw" + util.setcolor("white") + " | "

    if currentScreen == 5:
        menuString = menuString + util.setcolor("yellow")
    menuString = menuString + "(5) 0-100 Times" + util.setcolor("white") + " | "

    menuString = menuString + "(Q) Quit | "

    if replayMode == 0:
        if recordingStatus == 1:
            menuString = menuString + util.setcolor("green")
        else:
            menuString = menuString + util.setcolor("red")
    menuString = menuString + "(R) Record/Stop" + util.setcolor("white") + " | "

    if replayMode == 1:
        menuString = menuString + util.setcolor("yellow") + "(L) Load" + util.setcolor("white") + "\n"
    else:
        menuString = menuString + "(L) Load\n"


    print(menuString, flush=True)

def clearScreen(args):
    os.system("") #needed to enable ansi codes. also removes flicker for git bash clear
    if args.isgitbash:
        os.system("clear") #less flicker than cls
        print('\033[?25l', end="")  #hide cursor to prevent flashing. idk why this ansi code works but not clear screen...
    else:
        #os.system("cls")
        print("\x1b[2J")
        print("\x1b[H")
        print('\033[?25l', end="")  #hide cursor to prevent flashing. idk why this ansi code works but not clear screen...

    showMenu(args)

def readInput(args):
    if msvcrt.kbhit():
        getch = msvcrt.getch()
        num = ord(getch)
        #print("key ord is:" + str(num))


        global currentScreen
        global recordingStatus
        global replayMode
        global cursorPos
        global selected
        global skipAhead
        global toggleAccelerometer
        global togglePowerband

        if num == 49: #1 button
            currentScreen = 1

        elif num == 50: #2 button
            currentScreen = 2

        elif num == 51: #3 button
            currentScreen = 3

        elif num == 52: #4 button
            currentScreen = 4

        elif num == 53: #5button
            currentScreen = 5

        elif num == 113: #q button
            util.quit(args)

        elif num == 114 and replayMode == 0: #r button
            if recordingStatus == 1:
                recordingStatus = 0
                saveLogFile(args)
            else:
                recordingStatus = 1
        elif num == 114 and replayMode == 1:
            replayMode = 0

        elif num == 108: #l button
            replayMode = 1
            currentScreen = 0
            cursorPos = 0

        elif num == 80: # down
            cursorPos = cursorPos + 1

        elif num == 72 and cursorPos > 0: #up
            cursorPos = cursorPos -1

        elif num == 13: #/r
            selected = 1

        elif num == 77: #right arrow
            skipAhead = 1

        elif num == 116: #t button
            if currentScreen == 2:
                if toggleAccelerometer == 1:
                    toggleAccelerometer = 0
                else:
                    toggleAccelerometer = 1
            elif currentScreen == 5:
                if togglePowerband == 1:
                    togglePowerband = 0
                else:
                    togglePowerband = 1

cursorPos = 0
def showLoadMenu(args):
    global cursorPos
    global selected
    global currentScreen

    files = os.listdir("logs/")
    filesToShow = [] #lets only showfiles of the current config, cba allowing config change during runtime
    for file in files:
        if file.startswith(args.config) and file.endswith(".log"):
            filesToShow.append("\t" + file)

    lenFts = len(filesToShow)
    clearScreen(args)

    if lenFts > 0:
        if cursorPos >= lenFts:
            cursorPos = lenFts -1

        unalteredEntry = filesToShow[cursorPos]
        filesToShow[cursorPos] = util.setcolor("yellow") + ">" + filesToShow[cursorPos]   + util.setcolor("white")
        fileString = util.listToString(filesToShow, True)
        print(fileString)

        if selected == 1:
            selected = 0
            currentScreen = 2
            loadReplay(unalteredEntry.strip(), args)


    else:
        print("No recordings found in ./logs")

def loadReplay(filename, args):
    global replayMode
    global skipAhead

    dir = "logs/"
    if os.path.isfile(dir + filename):

        file = open(dir + filename, "r")
        lines = file.readlines()
        lineCount = len(lines)

        print("playing replay: " + filename + " (" + str(lineCount) + " lines)")

        skipCount = 0
        for lineNr in range(lineCount):
            if replayMode == 1: #allows us to interrupt replays
                correctedLineNumber = lineNr + skipCount

                if skipAhead == 1: #fast forward some frames
                    skipCount = skipCount + 100
                    skipAhead = 0

                if correctedLineNumber >= lineCount:
                    break

                clean = ast.literal_eval(lines[correctedLineNumber])
                interpret.interpretPacket(clean, args)

                if args.isgitbash:
                    time.sleep(0.01) # adjust to speed of normal program. prob wildy diff per pc. aiming for time between frames of 0.05 - 0.06
                else:
                    time.sleep(0.03)
                print("Replay progress: "+ str(correctedLineNumber) + "/" + str(lineCount))


    replayMode = 0

loggedFrames = []
def logFrame(data):
    loggedFrames.append(data)

def saveLogFile(args):
    if loggedFrames != []:
        dir = "logs/"

        if not os.path.exists(dir):
            os.mkdir(dir)

        filename = dir + args.config + "_" + str(round(time.time())) + ".log"

        print("Saving " + str(len(loggedFrames)) + " Frames to " + filename)

        logContents = util.listToString(loggedFrames, True)
        loggedFrames.clear()

        file = open(filename, "w")
        file.write(logContents)
        file.close()

def updateSuspensionCatalogue(car, surface, minF, maxF, minB, maxB):
    catalogue = "SuspensionCatalogue.json"

    if os.path.isfile(catalogue):
        file = open(catalogue, "r", encoding="utf-8")
        content = json.loads(file.read())

        carFound = False
        for carEntry in content:
            #update a car
            if carEntry["car"] == car:
                carEntry[surface + "MinF"] = minF
                carEntry[surface + "MaxF"] = maxF
                carEntry[surface + "MinB"] = minB
                carEntry[surface + "MaxB"] = maxB
                carFound = True

        if not carFound:
            #add a new car
            entry = {
                "car" : car,
                "name": util.resolveId(car, "vehicles"),
                surface + "MinF": minF,
                surface + "MaxF": maxF,
                surface + "MinB": minB,
                surface + "MaxB": maxB
            }
            content.append(entry)

        file.close()
        file = open(catalogue, "w", encoding="utf-8")
        #write modified content back
        file.write(json.dumps(content))
        file.close()

    else:
        #construct basic json to write:
        jsondata = []
        entry = {
            "car" : car,
            "name": util.resolveId(car, "vehicles"),
            surface + "MinF": minF,
            surface + "MaxF": maxF,
            surface + "MinB": minB,
            surface + "MaxB": maxB
        }

        jsondata.append(entry)

        #write new file
        file = open(catalogue, "a+", encoding="utf-8")
        file.write(json.dumps(jsondata))
        file.close()


def getSuspensionCatalogue():
    catalogue = "SuspensionCatalogue.json"
    content = []

    if os.path.isfile(catalogue):
        file = open(catalogue, "r", encoding="utf-8")
        content = json.loads(file.read())
        file.close()

    return content

def updatePBTable(packet):
    table = "TimesDatabase.csv"

    if "stage_result_time" in packet and os.path.isfile(table):

        #api on a version that supports this (1.8.0 +)
        location = packet["location_id"]
        locationName = util.resolveId(location, "locations")
        route = packet["route_id"]
        routeName = util.resolveId(route, "routes")
        gamemode = packet["game_mode"]
        gamemodeName = util.resolveId(gamemode, "game_mode")
        time = packet["stage_result_time"]
        timeReadable = util.pretty_print_time(time)
        penalty = packet["stage_result_time_penalty"]
        status = packet["stage_result_status"]
        vehicle = packet["vehicle_id"]
        vehicleName = util.resolveId(vehicle, "vehicles")
        carclass = packet["vehicle_class_id"]
        carclassName = util.resolveId(carclass, "vehicle_classes")
        manufacturer = packet["vehicle_manufacturer_id"]
        manufacturerName = util.resolveId(manufacturer, "vehicle_manufacturers")
        shakedown = packet["stage_shakedown"]
        packetkey = str(location) + "_" + str(route) + "_" + str(manufacturer) + "_" + str(vehicle) + "_" + str(carclass)
        packetRow = [location, locationName, route, routeName, manufacturer, manufacturerName, vehicle, vehicleName, carclass, carclassName, time, timeReadable, penalty, gamemodeName, str(datetime.datetime.now())]

        #only add when finished, not when dnf.
        if util.resolveId(status, "stage_result_status") == "finished" and shakedown == False and gamemodeName != "test_drive" and gamemodeName != "rally_school":

            rows = []
            with open(table, "r", encoding="utf-16") as file:
                reader = csv.reader(file)
                rows = list(reader)

            rowMatched = None
            overwrite = False
            counter = 0
            for row in rows:
                if row == [] or row == "":
                    continue

                rowkey = row[0] + "_" + row[2] + "_" + row[4] + "_" + row[6] + "_" + row[8]

                #check if value is already in the db
                if packetkey == rowkey:
                    rowMatched = counter
                    #update existing row if time is faster.
                    loggedTime = float(row[10])
                    time

                    if time < loggedTime:
                        overwrite = True
                        break

                counter = counter + 1


            if rowMatched == None:
                rows.append(packetRow)
            elif overwrite == True:
                rows[counter] = packetRow

            if rowMatched == None or overwrite == True:
                print("\n" + util.setcolor("green") + "Updating PB Database" + util.setcolor("white"))
                #remove empty rows if there are any:
                cleanrows = [row for row in rows if row != []]

                with open(table, "w", encoding="utf-16", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerows(cleanrows)


lastReadRows = []
lastReadTime = 0
def getPB(packet):
    global lastReadRows
    global lastReadTime
    pbCheckCacheTime = 10 #seconds

    currentTime = time.time()

    pbtime = ""
    table = "TimesDatabase.csv"

    if "stage_result_time" in packet and os.path.isfile(table):

        #api on a version that supports this (1.8.0 +)
        location = packet["location_id"]
        route = packet["route_id"]
        vehicle = packet["vehicle_id"]
        carclass = packet["vehicle_class_id"]
        manufacturer = packet["vehicle_manufacturer_id"]
        packetkey = str(location) + "_" + str(route) + "_" + str(manufacturer) + "_" + str(vehicle) + "_" + str(carclass)


        if (currentTime - lastReadTime) > pbCheckCacheTime:
            with open(table, "r", encoding="utf-16") as file:
                reader = csv.reader(file)
                lastReadRows = list(reader)
                lastReadTime = currentTime
        
        for row in lastReadRows:
            if row == [] or row == "":
                continue

            rowkey = row[0] + "_" + row[2] + "_" + row[4] + "_" + row[6] + "_" + row[8]
            if packetkey == rowkey:
                loggedTime = float(row[10])
                pbtime = util.pretty_print_time(loggedTime)
                break
    return pbtime