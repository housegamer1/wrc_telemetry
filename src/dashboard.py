import util   
import inout

def _visPedal(data, color):
    returnstring = util.setcolor("white") + "[" + util.setcolor(color)
    counter = 0.0
    
    #pedal position in "=" characters / 10
    while counter < data:
        returnstring = returnstring + "="
        counter = counter + 0.1
    
    #fill rest with spaces
    while counter < 1.0:
        returnstring = returnstring + " "
        counter = counter + 0.1

    return returnstring + util.setcolor("white") + "]" 

def _steerRight(data):
    returnstring = _steer(data)

    #add right spaces
    while len(returnstring) < 10:
        returnstring = returnstring + " "

    #add middle 
    returnstring = "          =" + returnstring 

    return returnstring

def _steerLeft(data):
    returnstring = _steer(data)

    #add left spaces
    while len(returnstring) < 10:
        returnstring = " " + returnstring

    #add middle 
    returnstring = returnstring + "="

    #fill rest with spaces
    return returnstring + "          "

def _steer(data):
    data = abs(data)
    returnstring = ""
    counter = 0.0

    while counter < data:
        returnstring = returnstring + "="
        counter = round(counter + 0.1, 1) #no need to stretch the indicator to twice the length. round to avoid 0.00000000000000001 errors
    
    return returnstring

def _visSteering(data):
    #TODO: shows one bar later to the left as to the right
    returnstring = "["

    if data > 0.0:
        returnstring = returnstring + _steerRight(data)

    elif data < 0.0: #left steer
        returnstring = returnstring + _steerLeft(data)

    elif data == 0.0: #no steering
        returnstring = returnstring + "          =          "

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

    returnstring = util.setcolor("white") + "["

    counter = 0.0
    while counter < rpmPercent:
        if counter > 0.8:
            returnstring = returnstring + util.setcolor("red") + "="
        elif counter > 0.6:
            returnstring = returnstring + util.setcolor("yellow") + "="
        else :
            returnstring = returnstring + "="
        
        counter = counter + 0.1

    #fill rest with space
    while counter < 1.0:
        returnstring = returnstring + " "
        counter = counter + 0.1

    return returnstring + util.setcolor("white") + "]\t" + str(currentRpm) + "/" + str(maxRpm)

def _applyTempColor(temperature):
    #Highest brake temp i could force was like 600

    if temperature <= 0:
        return util.setcolor("purple")
    elif temperature < 75:      #0-75
        return util.setcolor("blue")
    elif temperature < 250:     #75 - 250
        return util.setcolor("green")
    elif temperature < 400:     #250 -400
        return util.setcolor("yellow")
    elif temperature > 400:     #400 - inf
        return util.setcolor("red")
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

    returnstring = "FL [" + flColor + "||" + util.setcolor("white") +"] " + str(fl) + "\t FR [" + frColor + "||" + util.setcolor("white") + "] " + str(fr) + "\n"
    returnstring = returnstring + "\t\t\tRL [" + blColor + "||" + util.setcolor("white") + "] " + str(bl) + "\t RR [" + brColor + "||" + util.setcolor("white") + "] " + str(br)

    return returnstring

def _visTireState(packet):
    fr = packet["vehicle_tyre_state_fr"]
    fl = packet["vehicle_tyre_state_fl"]
    br = packet["vehicle_tyre_state_br"]
    bl = packet["vehicle_tyre_state_bl"]

    statusFr = util.resolveId(fr, "vehicle_tyre_state")
    statusFl = util.resolveId(fl, "vehicle_tyre_state")
    statusBr = util.resolveId(br, "vehicle_tyre_state")
    statusBl = util.resolveId(bl, "vehicle_tyre_state")

    frColor = _applyTireStatusColor(statusFr)
    flColor = _applyTireStatusColor(statusFl)
    brColor = _applyTireStatusColor(statusBr)
    blColor = _applyTireStatusColor(statusBl)

    returnstring = "FL [" + flColor + statusFl + util.setcolor("white") +"]\t FR [" + frColor + statusFr + util.setcolor("white") + "]\n"
    returnstring = returnstring + "\t\tRL [" + blColor + statusBl + util.setcolor("white") + "]\t RR [" + brColor + statusBr + util.setcolor("white") + "]"
    
    return returnstring

def _applyTireStatusColor(status):
    if status == "undamaged":
        return util.setcolor("green")
    elif status == "punctured":
        return util.setcolor("yellow")
    elif status == "burst":
        return util.setcolor("red")
    
    #shouldnt happen
    return util.setcolor("white")


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
    global previousData

    width = 30 #equal to age 
    if inout.toggleAccelerometer == 0:
        width = 90

    if width == 30 and len(previousData) > 30:
        previousData.clear()

    height = 11 #11 so WOT (10) will not out of bounds
    
    dataPoint = {
        "throttle" : 10 - round(throttle *10), #value comes as 0.0 - 1.0
        "brake" : 10 - round(brake * 10)
    }


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
        graph[dpT][counter] = util.setcolor("green") + charToDraw["throttle"] + util.setcolor("white")
        graph[dpB][counter] = util.setcolor("red") + charToDraw["brake"] + util.setcolor("white")
        counter = counter + 1        
        lastDatapointDrawn = dp

    #build return
    returnstring = ""
    firstRow = True
    for row in graph:
        if firstRow:
            returnstring = returnstring + util.listToString(row, False)
            firstRow = False
        else:
            returnstring = returnstring + "\t\t" + util.listToString(row, False)
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
        returnstring = returnstring + "\t\t" + util.listToString(row, False)
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


def visualizePacket(packet, fancy):
    
    printstring = ""

    #TODO could do science with diff setting vs cp (contact patch) speed
    car = ""
    manufacturer = ""
    carclass = ""
    location = ""
    stage = ""

    if "vehicle_id" in packet:
        car = util.resolveId(packet["vehicle_id"], "vehicles")

    if "location_id" in packet:
        location = util.resolveId(packet["location_id"], "locations")

    if "route_id" in packet:
        stage = util.resolveId(packet["route_id"], "routes")

    if car != "" or location != "" or stage != "":
        printstring = printstring + car + " | " + location + " " + stage + "\n\n"

    if "vehicle_throttle" in packet:
        printstring = printstring + ">>>   Throttle:\t\t" + _visPedal(packet["vehicle_throttle"], "green") + "\t"

    if "vehicle_brake" in packet:
        printstring = printstring + ">>>   Brake:\t\t" + _visPedal(packet["vehicle_brake"], "red") + "\n"

    if "vehicle_clutch" in packet:        
        printstring = printstring + ">>>   Clutch:\t\t" + _visPedal(packet["vehicle_clutch"], "white") + "\t"

    if "vehicle_handbrake" in packet:
        printstring = printstring + ">>>   Handbrake:\t" + _visPedal(packet["vehicle_handbrake"], "red") + "\n\n"

    if "stage_current_distance" in packet and "stage_length" in packet:
        printstring = printstring + ">>>   Distance:\t\t" + str(util.mToKm(packet["stage_current_distance"])) + "/" + str(util.mToKm(packet["stage_length"])) + " km\t"

    if "vehicle_steering" in packet:    
        printstring = printstring + ">>>   Steering:\t\t" + _visSteering(packet["vehicle_steering"]) + "\n\n"

    if "vehicle_gear_maximum" in packet and "vehicle_gear_index" in packet and "vehicle_gear_index_reverse" in packet and "vehicle_gear_index_neutral" in packet:
        printstring = printstring + ">>>   Gear:\t\t" + _visGear(packet) + "\t\t"

    if "vehicle_engine_rpm_current" in packet and "vehicle_engine_rpm_max" in packet and "shiftlights_fraction" in packet:
        printstring = printstring + ">>>   RPM:\t\t" + _visRpm(packet) + "\n"

    if "vehicle_transmission_speed" in packet and "vehicle_speed" in packet:
        transspeed = packet["vehicle_transmission_speed"]
        gpsspeed = packet["vehicle_speed"]

        slip = ""
        if transspeed > gpsspeed * 1.25: #should roughly take care of the losses. but gets unreliable at high speed
            slip = util.setcolor("purple") + "**SLIP**"+ util.setcolor("white") 
        elif transspeed < gpsspeed * 0.5: 
            slip = util.setcolor("purple") + "**LOCKUP**"+ util.setcolor("white") 

        if packet["vehicle_speed"] >= 100:
            printstring = printstring + ">>>   Gps Speed:\t" + str(packet["vehicle_speed"]) + " Km/h\t" #otherwise it pops to the right when we go over 100.
        else:
            printstring = printstring + ">>>   Gps Speed:\t" + str(packet["vehicle_speed"]) + " Km/h\t\t"

        printstring = printstring + ">>>   Trans Speed:\t" + str(packet["vehicle_transmission_speed"]) + " Km/h  " + slip + "\n"
        

    tireString = ""
    if "vehicle_tyre_state_bl" in packet and "vehicle_tyre_state_br" in packet and "vehicle_tyre_state_fl" in packet and "vehicle_tyre_state_fr" in packet:
        tireString = "Tire status:\t" + _visTireState(packet)

    brakeString = ""
    if "vehicle_brake_temperature_bl" in packet and "vehicle_brake_temperature_br" in packet and "vehicle_brake_temperature_fl" in packet and "vehicle_brake_temperature_fr" in packet:
        brakeString = ">>>   Brake Temp:\t" + _visBrakeTemp(packet)

    printstring = printstring + util.drawSideBySide(brakeString, tireString) + "\n\n"

    printstring = printstring + ">>>   Press (T) to toggle accelerometer\n"
    histoString = ""
    if fancy and "vehicle_throttle" in packet and "vehicle_brake" in packet:
        histoString = ">>>   Histo:\t" + _visHisto(packet["vehicle_throttle"], packet["vehicle_brake"]) #no newline as it comes from the graph already

    accelstring = ""
    if inout.toggleAccelerometer == 1 and fancy and "vehicle_acceleration_x" in packet and "vehicle_acceleration_z" in packet: #y is up down

        reset = 1
        if "stage_current_distance" in packet:
            reset = packet["stage_current_distance"] #reset max g logger on restart, default: never reset

        accelstring = ">>>   Accel:\t" + _visAccel(packet["vehicle_acceleration_z"], packet["vehicle_acceleration_x"], reset) + "\n"
        
    if histoString != "" or accelstring != "":
        printstring = printstring + util.drawSideBySide(histoString, accelstring)

    print(printstring)