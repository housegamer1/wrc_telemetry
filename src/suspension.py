import util

def _visHubPosition(pos):
    height = 21 #lets go from -20 to + 20. means we jump for every 2cm
    graph = ["\t .\n" for x in range(height)]

    counter = 0
    value = 20
    while value > pos:
        #graph[counter] = "\t" + str(value) + "\n" #print values above slider for testing

        value = value -2
        counter = counter + 1

        #check after change
        if value <= pos:
            break

        if counter == height -1:
            break

        
    #replace position in graph
    if counter <= 4 or counter >= (height - 5):
        graph[counter] = util.setcolor("purple") + "\t" + str(pos) + util.setcolor("white") +" \n"
    else:
        graph[counter] = util.setcolor("yellow") + "\t" + str(pos) + util.setcolor("white") +" \n"


    returnstring = util.listToString(graph, False)
    return returnstring



stageStarted=0
minmax = {
    "maxFl":0,
    "minFl":0,
    "maxFr":0,
    "minFr":0,
    "maxBl":0,
    "minBl":0,
    "maxBr":0,
    "minBr":0
}
wheelHubPositionMemory = {
    "Fl" : [],
    "Fr" : [],
    "Bl" : [],
    "Br" : []
}

def showCurrentAndMax(pos, wheel):
    global minmax
    global wheelHubPositionMemory

    rpos = round(pos)
    
    #record all known values so we can later calculate the average
    wheelHubPositionMemory[wheel].append(rpos)    

    max = minmax["max" + wheel]
    min = minmax["min" + wheel]
    newmaxColor = ""
    newminColor = ""
    if rpos > max:
        minmax["max" + wheel] = rpos
        max = rpos
        newmaxColor = util.setcolor("purple")
    elif rpos < min:
        minmax["min" + wheel] = rpos
        min = rpos
        newminColor = util.setcolor("purple")

    #negative two digit values just so happen to trigger the max length of tab
    #so that drawSideBySide adds another tab....
    posAdjust = " " if rpos >= 0 else ""
    maxAdjust = " " if max >= 0 else ""
    minAdjust = " " if min >= 0 else ""
    returnstring = "\tNOW:" + posAdjust + str(rpos) + "\n"
    returnstring = returnstring + "\tMAX:" + maxAdjust + newmaxColor + str(max) + util.setcolor("white") + "\n"
    returnstring = returnstring + "\tMIN:"  + minAdjust + newminColor + str(min) + util.setcolor("white") + "\n"
    returnstring = returnstring + "\tAVG:" + str(avgSuspensionPosition[wheel]) + "\n"

    return returnstring

blockAvgCalc = False
avgSuspensionPosition = {
    "Fl" : 0,
    "Fr" : 0,
    "Bl" : 0,
    "Br" : 0
}

def calcTravelAvg():
    wheels = ["Fl", "Fr", "Bl", "Br"]
    for wheel in wheels:
        suspensionPositions = wheelHubPositionMemory[wheel]
        length = len(suspensionPositions)

        if length > 0:
            avg = round(sum(suspensionPositions) / length)
            avgSuspensionPosition[wheel] = avg

        #reset the position memory, so that new avg calculations will be more usable for the driver. otherwise the value will pretty much never change
        wheelHubPositionMemory[wheel] = []


def visualizePacket(packet):
    requiredData = []
    requiredData.append("vehicle_hub_position_fl")
    requiredData.append("vehicle_hub_position_fr")
    requiredData.append("vehicle_hub_position_bl")
    requiredData.append("vehicle_hub_position_br")

    for needed in requiredData:
        if needed not in packet:
            print("required data not in packet:" + needed)
            return
        
    posFl = round(packet["vehicle_hub_position_fl"] * 100) # convert to cm
    posFr = round(packet["vehicle_hub_position_fr"] * 100)
    posBl = round(packet["vehicle_hub_position_bl"] * 100)
    posBr = round(packet["vehicle_hub_position_br"] * 100)

    if "stage_current_distance" in packet: 
        
        #reset minmax and wheel hub position counter if stagedistance is 0
        
        #lets only allow resetting if the stage was started previosly. i.e. distance > 0.
        #this stops the new maximum and new minimum color being constantly applied
        global stageStarted
        distance = packet["stage_current_distance"]
        
        if distance == 0 and stageStarted > 0:
            global minmax
            minmax = {
                    "maxFl":0,
                    "minFl":0,
                    "maxFr":0,
                    "minFr":0,
                    "maxBl":0,
                    "minBl":0,
                    "maxBr":0,
                    "minBr":0
            }

            global wheelHubPositionMemory
            wheelHubPositionMemory = {
                "Fl" : [],
                "Fr" : [],
                "Bl" : [],
                "Br" : []
            }

            stageStarted = 0
        elif distance > 0 and stageStarted == 0:
            stageStarted = distance


        #calculate average suspension travel for every completed KM of stage
        global blockAvgCalc                        
        kilometerModulo = round((util.mToKm(distance) % 1), 1)

        #print("distance modulo: " + str(kilometerModulo))
        #print("blockAvgCalc: " + str(blockAvgCalc))

        #use this global var so we only calculate once and not for every packet where the player is at the kilometer mark +- 20 meters
        #if the player stopped there, it would calculate this every time. Only when the modulo goes to > 0.0 again, we can unblock the calculation.
        
        if kilometerModulo == 0.0 and not blockAvgCalc:
            calcTravelAvg()
            blockAvgCalc = True
        elif kilometerModulo > 0.0:
            blockAvgCalc = False
            


    finalString = "Offset of wheel hub in wheel well in cm\n\n"
    posFlString = "\tFront Left\n"  + showCurrentAndMax(posFl, "Fl") + "\n" + _visHubPosition(posFl)
    posFrString = "Front Right\n" + showCurrentAndMax(posFr, "Fr") + "\n" + _visHubPosition(posFr)
    posBlString = "Back Left\n" + showCurrentAndMax(posBl, "Bl") + "\n" + _visHubPosition(posBl)
    posBrString = "Back Right\n" + showCurrentAndMax(posBr, "Br") + "\n" + _visHubPosition(posBr)

    frontString = util.drawSideBySide(posFlString, posFrString)
    backString = util.drawSideBySide(posBlString, posBrString)

    finalString = finalString + util.drawSideBySide(frontString, backString)    
    print(finalString)