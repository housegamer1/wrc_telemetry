import util
import queue

def visualize(packet, args):
    if args.debug:
        printPacket(packet, args)
    else:
        visualizePacket(packet, args)        

def _visPedal(data, color):
    returnstring = _setcolor("white") + "[" + _setcolor(color)
    counter = 0.0
    
    #pedal position in "=" characters / 10
    while counter < data:
        returnstring = returnstring + "="
        counter = counter + 0.1
    
    #fill rest with spaces
    while counter < 1.0:
        returnstring = returnstring + " "
        counter = counter + 0.1

    return returnstring + _setcolor("white") + "]" 

def _steerRight(data):
    returnstring = "     "
    counter = 0.0

    while counter < data:
        returnstring = returnstring + "="
        counter = round(counter + 0.2, 1) #no need to stretch the indicator to twice the length. round to avoid 0.00000000000000001 errors

    #add middle
    returnstring = returnstring + "="

    #fill rest with spaces
    while counter < 1.0:
        returnstring = returnstring + " "
        counter = round(counter + 0.2, 1)
    
    return returnstring

def _steerLeft(data):
    returnstring = ""
    counter = -0.9 #lame fix for being offset by one char in neg numbers
    while counter < data:
        returnstring = returnstring + " "
        counter = round(counter + 0.2, 1)

    #fill until 0 with "="
    while counter < 0.0:
        returnstring = returnstring + "="
        counter = round(counter + 0.2, 1)

    #add middle 
    returnstring = returnstring + "="

    #fill rest with spaces
    return returnstring + "     "

def _visSteering(data):
    #TODO: shows one bar later to the left as to the right
    returnstring = "["

    if data > 0.0:
        returnstring = returnstring + _steerRight(data)

    elif data < 0.0: #left steer
        returnstring = returnstring + _steerLeft(data)

    elif data == 0.0: #no steering
        returnstring = returnstring + "     =     "

    return returnstring + "]"

def _visGear(packet):
    maxGears = packet["vehicle_gear_maximum"]
    currentGear = packet["vehicle_gear_index"]
    reverse = packet["vehicle_gear_index_reverse"]
    neutral = packet["vehicle_gear_index_neutral"]

    if currentGear == reverse:
        return "R"
    elif currentGear == neutral:
        return "N"
    else:
        return str(currentGear) + "/" + str(maxGears)
    
def _visRpm(packet):
    currentRpm = packet["vehicle_engine_rpm_current"]
    maxRpm = packet["vehicle_engine_rpm_max"]
    rpmPercent = packet["shiftlights_fraction"]

    returnstring = _setcolor("white") + "["

    counter = 0.0
    while counter < rpmPercent:
        if counter > 0.8:
            returnstring = returnstring + _setcolor("red") + "="
        elif counter > 0.6:
            returnstring = returnstring + _setcolor("yellow") + "="
        else :
            returnstring = returnstring + "="
        
        counter = counter + 0.1

    #fill rest with space
    while counter < 1.0:
        returnstring = returnstring + " "
        counter = counter + 0.1

    return returnstring + _setcolor("white") + "]\t" + str(currentRpm) + "/" + str(maxRpm)

def _applyTempColor(temperature):
    #Highest brake temp i could force was like 600

    if temperature <= 0:
        return _setcolor("purple")
    elif temperature < 75:      #0-75
        return _setcolor("blue")
    elif temperature < 250:     #75 - 250
        return _setcolor("green")
    elif temperature < 400:     #250 -400
        return _setcolor("yellow")
    elif temperature > 400:     #400 - inf
        return _setcolor("red")
    else:
        return ""

def _visBrakeTemp(packet):
    fr = packet["vehicle_brake_temperature_fr"]
    fl = packet["vehicle_brake_temperature_fl"]
    br = packet["vehicle_brake_temperature_br"]
    bl = packet["vehicle_brake_temperature_bl"]

    frColor = _applyTempColor(fr)
    flColor = _applyTempColor(fl)
    brColor = _applyTempColor(br)
    blColor = _applyTempColor(bl)

    returnstring = "FL [" + flColor + "||" + _setcolor("white") +"] " + str(fl) + "\t FR [" + frColor + "||" + _setcolor("white") + "] " + str(fr) + "\n"
    returnstring = returnstring + "\t\t\tRL [" + blColor + "||" + _setcolor("white") + "] " + str(bl) + "\t RR [" + brColor + "||" + _setcolor("white") + "] " + str(br)

    return returnstring

def _pickCharToDraw(dp, oldDp):
    chars = {
        "throttle": "_",
        "brake": "_"
    }

    if oldDp == {}:
        return chars        

    dpT = dp["throttle"]
    dpB = dp["brake"]
    odpT = oldDp["throttle"]
    odpB = oldDp["brake"]

    #print("dpt: " + str(dpT) + " old dpt: "+ str(odpT))

    if dpT != 0 and dpT != 10: #dont depict rising if max already reached this tick
        #inverse logic as the graph flipped the values to that 0/0 coord is bottom left
        if dpT < odpT: 
            chars["throttle"] = "/"
        elif dpT > odpT:
            chars["throttle"] = "\\"
        else:
            chars["throttle"] = "_"

    if dpB != 0  and dpB != 10:
        if dpB < odpB: 
            chars["brake"] = "/"
        elif dpB > odpB:
            chars["brake"] = "\\"
        else:
            chars["brake"] = "_"   

    return chars

previousData = []
def _visHisto(throttle, brake):
    width = 30 #equal to age 
    height = 11 #11 so WOT (10) will not out of bounds
    
    dataPoint = {
        "throttle" : 10 - round(throttle *10), #value comes as 0.0 - 1.0
        "brake" : 10 - round(brake * 10)
    }

    global previousData

    if len(previousData) == width:
        #buffer is full, remove old entry, copy to new list
        previousData.pop(0)
        newHist = []
        for entry in previousData:
            newHist.append(entry)
        previousData = newHist

    previousData.append(dataPoint) #append current data point

    graph = [[" " for x in range(width)] for y in range(height)] # draw empty graph
    
    #draw graph
    amountOfSkippedFields = width - len(previousData)
    counter = 0
    lastDatapointDrawn = {}
    for dp in previousData:
        while counter < amountOfSkippedFields: #fast forward to the columns we need to draw
            counter = counter + 1
            continue

        dpT = dp["throttle"] 
        dpB = dp["brake"]

        charToDraw = _pickCharToDraw(dp, lastDatapointDrawn)

        #idk why x and y flipped but it works lol
        graph[dpT][counter] = _setcolor("green") + charToDraw["throttle"] + _setcolor("white")
        graph[dpB][counter] = _setcolor("red") + charToDraw["brake"] + _setcolor("white")
        counter = counter + 1        
        lastDatapointDrawn = dp

    #build return
    returnstring = ""
    firstRow = True
    for row in graph:
        if firstRow:
            returnstring = returnstring + util.listToString(row)
            firstRow = False
        else:
            returnstring = returnstring + "\t\t" + util.listToString(row)
        returnstring = returnstring + "\n"

    return returnstring

previousAccel = []
maxGfw = 0
maxGsw = 0
def _visAccel(fw, sw, resetMaxG):

    width = 30 
    height = 10

    graph = [["." for x in range(width)] for y in range(height)] # draw empty graph

    #draw trail
    global previousAccel
    for point in previousAccel:
        graph[point["fw"]][point["sw"]] = "-"

    centerFw = round(height / 2)
    centerSw = round(width /2)

    adjustFw = round(fw / 9.81, 1) #these are m/s² so convert to g
    adjustSw = round(sw / 9.81, 1) 

    #offset from center and pronounce visualisation.
    #pronounce sw a lot more, since the graph is 3:1 stretched
    newFw = centerFw + round(adjustFw * 2)
    newSw = centerSw + round(adjustSw * 6) 

    #cap the values
    newFw = newFw if newFw < height else (height -1)
    newSw = newSw if newSw < width else (width -1)
    newFw = newFw if newFw > 0 else 0
    newSw = newSw if newSw > 0 else 0

    #print("[newFw][newSw] = [" + str(newFw) + "][" + str(newSw) + "]")
    graph[newFw][newSw] = "+"

    global maxGfw
    global maxGsw

    if(resetMaxG == 0):
        #stagedistance is 0 so reset the maxcounter for restarts
        maxGfw = 0
        maxGsw = 0

    if abs(adjustFw) > abs(maxGfw):
        maxGfw = adjustFw
    
    if abs(adjustSw) > abs(maxGsw):
        maxGsw = adjustSw

    returnstring = "Fw: " + str(adjustFw) + "g (max: " + str(maxGfw) + ") Sw: " + str(adjustSw) + "g (max: " + str(maxGsw) + ")\t\n"
    for row in graph:
        returnstring = returnstring + "\t\t" + util.listToString(row)
        returnstring = returnstring + "\n"

    datapoint = {
        "fw" : newFw,
        "sw" : newSw
    }

    previousAccel.append(datapoint)
    if len(previousAccel) >= 8: #8~looks okay
        previousAccel.pop(0)
        newHist = []
        for entry in previousAccel:
            newHist.append(entry)
        previousAccel = newHist

    return returnstring

def _setcolor(color):
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
    
def _drawSideBySide(leftDraw, rightDraw):
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


    # for lLine in longer:
    #     returnstring = returnstring + lLine

    #     if counter < len(shorter):
    #         returnstring = returnstring + "\t" + shorter[counter]

    #     counter = counter +1
    #     returnstring = returnstring + "\n"
    return returnstring


def visualizePacket(packet, args):
    util.clearScreen(args.isgitbash)

    if args.isgitbash:
        print('\033[?25l', end="")  #hide cursor to prevent flashing. idk why this ansi code works but not clear screen...
    
    printstring = ""

    #TODO could do science with diff setting vs cp (contact patch) speed
    #TODO could do science with damper setting vs hub speed and position

    if "vehicle_throttle" in packet:
        printstring = ">>>   Throttle:\t\t" + _visPedal(packet["vehicle_throttle"], "green") + "\t"

    if "vehicle_brake" in packet:
        printstring = printstring + ">>>   Brake:\t\t" + _visPedal(packet["vehicle_brake"], "red") + "\n"

    if "vehicle_clutch" in packet:        
        printstring = printstring + ">>>   Clutch:\t\t" + _visPedal(packet["vehicle_clutch"], "white") + "\t"

    if "vehicle_handbrake" in packet:
        printstring = printstring + ">>>   Handbrake:\t" + _visPedal(packet["vehicle_handbrake"], "red") + "\n\n"

    if "vehicle_steering" in packet:    
        printstring = printstring + ">>>   Steering:\t\t" + _visSteering(packet["vehicle_steering"]) + "\t"

    if "stage_current_distance" in packet and "stage_length" in packet:
        printstring = printstring + ">>>   Distance:\t\t" + str(util.mToKm(packet["stage_current_distance"])) + "/" + str(util.mToKm(packet["stage_length"])) + " km\n\n"

    if "vehicle_gear_maximum" in packet and "vehicle_gear_index" in packet and "vehicle_gear_index_reverse" in packet and "vehicle_gear_index_neutral" in packet:
        printstring = printstring + ">>>   Gear:\t\t" + _visGear(packet) + "\t\t"

    if "vehicle_engine_rpm_current" in packet and "vehicle_engine_rpm_max" in packet and "shiftlights_fraction" in packet:
        printstring = printstring + ">>>   RPM:\t\t" + _visRpm(packet) + "\n"

    if "vehicle_transmission_speed" in packet and "vehicle_speed" in packet:
        transspeed = packet["vehicle_transmission_speed"]
        gpsspeed = packet["vehicle_speed"]

        slip = ""
        if transspeed > gpsspeed * 1.25: #should roughly take care of the losses. but gets unreliable at high speed
            slip = _setcolor("purple") + "**SLIP**"+ _setcolor("white") 
        elif transspeed < gpsspeed * 0.5: 
            slip = _setcolor("purple") + "**LOCKUP**"+ _setcolor("white") 

        printstring = printstring + ">>>   Gps Speed:\t" + str(packet["vehicle_speed"]) + " Km/h\t\t"
        printstring = printstring + ">>>   Trans Speed:\t" + str(packet["vehicle_transmission_speed"]) + " Km/h  " + slip + "\n"
        

    if "vehicle_brake_temperature_bl" in packet and "vehicle_brake_temperature_br" in packet and "vehicle_brake_temperature_fl" in packet and "vehicle_brake_temperature_fr" in packet:
        printstring = printstring + ">>>   Brake Temp:\t" + _visBrakeTemp(packet) + "\n\n"


    histoString = ""
    if args.fancy and "vehicle_throttle" in packet and "vehicle_brake" in packet:
        histoString = ">>>   Histo:\t" + _visHisto(packet["vehicle_throttle"], packet["vehicle_brake"]) #no newline as it comes from the graph already

    accelstring = ""
    if args.fancy and "vehicle_acceleration_x" in packet and "vehicle_acceleration_z" in packet: #y is up down

        reset = 1
        if "stage_current_distance" in packet:
            reset = packet["stage_current_distance"] #reset max g logger on restart, default: never reset

        accelstring = ">>>   Accel:\t" + _visAccel(packet["vehicle_acceleration_z"], packet["vehicle_acceleration_x"], reset) + "\n"
        
    if histoString != "" or accelstring != "":
        printstring = printstring + _drawSideBySide(histoString, accelstring)

    print(printstring)


def printPacket(packet, args):
    util.clearScreen(args.isgitbash)

    if args.isgitbash:
        print('\033[?25l', end="")  #hide cursor to prevent flashing. idk why this ansi code works but not clear screen...

    printstring = ">>>   "
    count = 0
    for field in packet:  
        count = count + 1
        printstring = printstring + str(field) + ": " + str(packet[field]) + " | "
        if count == 3:
            printstring = printstring + "\n>>>   "
            count = 0
    
    print(printstring)