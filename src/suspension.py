import util
import inout

def _visHubPosition(pos, axle):
    height = 21 #lets go from -20 to + 20. means we jump for every 2cm
    graph = [util.setcolor("white") + "\t |\n" for x in range(height)]

    currentCatalogue = inout.getSuspensionCatalogue()

    if currentCar != "" and surfaceType != "":
        for entry in currentCatalogue:
            if entry["car"] == currentCar:
                if pos <= int(entry[surfaceType + "Min" + axle]):
                    #(close to) no road contact!
                    graph = [util.setcolor("blue") + "\t |\n" + util.setcolor("white") for x in range(height)]
                    break
                elif pos >= int(entry[surfaceType + "Max" + axle] -1):
                    #(close to) bottoming out!
                    graph = [util.setcolor("red") + "\t |\n" + util.setcolor("white") for x in range(height)]
                    break

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



def resetStoredValues():
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

    global stageStarted
    stageStarted = 0

def setCarAndSurface(packet):
    #for recording the suspension travel of every individual car
    global currentCar
    global surfaceType

    if "vehicle_id" in packet and "location_id" in packet:
        currentCar = packet["vehicle_id"]
        currentLocation = packet["location_id"]

        if currentLocation == 5 or currentLocation == 16 or currentLocation == 17 or currentLocation == 25 or currentLocation == 28 or currentLocation == 29:
            #mediterraneo, croatia, monte carlo, japan, iberia, cer.
            #we need to check this, because ride heights / actual suspension components and wheels are different for tarmac locations.
            surfaceType = "Tarmac"
        else:
            surfaceType = "Loose"


def prepCatalogueUpdate():
    #for simplicity reasons we only track one wheel front and back and assume all wheels on the same axle have the same range of motion

    global currentCar
    global surfaceType
    global minmax

    if currentCar != "":
        minimumFront = minmax["minFl"]
        maximumFront = minmax["maxFl"]
        minimumBack = minmax["minBr"]
        maximumBack = minmax["maxBr"]

        currentCatalogue = inout.getSuspensionCatalogue()

        for carEntry in currentCatalogue:

            if carEntry["car"] == currentCar:
                #car exists. check if values for this surface are now more extreme

                if surfaceType + "MinF" in carEntry:
                    existingMinFront = int(carEntry[surfaceType + "MinF"])
                    existingMaxFront = int(carEntry[surfaceType + "MaxF"])
                    existingMinBack = int(carEntry[surfaceType + "MinB"])
                    existingMaxBack = int(carEntry[surfaceType + "MaxB"])

                    if existingMinFront <= minimumFront and existingMaxFront >= maximumFront and existingMinBack <= minimumBack and existingMaxBack >= maximumBack:
                        return

                    minimumFront = min(minimumFront, existingMinFront)
                    maximumFront = max(maximumFront, existingMaxFront)
                    minimumBack = min(minimumBack, existingMinBack)
                    maximumBack = max(maximumBack, existingMaxBack)

        inout.updateSuspensionCatalogue(currentCar, surfaceType, minimumFront, maximumFront, minimumBack, maximumBack)

def oncePerKmAction():
    calcTravelAvg()
    prepCatalogueUpdate()

currentCar = ""
surfaceType = ""
def visualizePacket(packet, hide):
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
        
        global stageStarted
        distance = packet["stage_current_distance"]
        
        if currentCar == "":
            #only need to set the car on stage starts
            setCarAndSurface(packet)        

        if distance == 0 and stageStarted > 0:
                #reset minmax and wheel hub position counter if stagedistance is 0        
                #lets only allow resetting if the stage was started previosly. i.e. distance > 0.
                #this stops the new maximum and new minimum color being constantly applied

                prepCatalogueUpdate() #dont delete things if we hit restart, instead use the already gathered values.
                resetStoredValues()
                setCarAndSurface(packet) #could have switched to a different stage now.
        elif distance > 0 and stageStarted == 0:
            #stage was started, detect it by using the distance.
            #this way we can tell if we are a clean start or a restart
            stageStarted = distance



        #calculate average suspension travel for every completed KM of stage
        #use this global var so we only calculate once and not for every packet where the player is at the kilometer mark +- 20 meters
        #if the player stopped there, it would calculate this every time. Only when the modulo goes to > 0.0 again, we can unblock the calculation.
        global blockAvgCalc                        
        kilometerModulo = round((util.mToKm(distance) % 1), 1)
            
        
        if kilometerModulo == 0.0 and not blockAvgCalc:
            oncePerKmAction()
            blockAvgCalc = True
        elif kilometerModulo > 0.0:
            blockAvgCalc = False


    finalString = "Offset of wheel hub in wheel well in cm. " + util.setcolor("blue") + "|" + util.setcolor("white") +" = No road contact, " + util.setcolor("red") + "|" + util.setcolor("white") + " = Bottoming out (program learns with time)\n\n"
    posFlString = "\tFront Left\n"  + showCurrentAndMax(posFl, "Fl") + "\n" + _visHubPosition(posFl, "F")
    posFrString = "Front Right\n" + showCurrentAndMax(posFr, "Fr") + "\n" + _visHubPosition(posFr, "F")
    posBlString = "Back Left\n" + showCurrentAndMax(posBl, "Bl") + "\n" + _visHubPosition(posBl, "B")
    posBrString = "Back Right\n" + showCurrentAndMax(posBr, "Br") + "\n" + _visHubPosition(posBr, "B")

    if not hide:
        frontString = util.drawSideBySide(posFlString, posFrString)
        backString = util.drawSideBySide(posBlString, posBrString)

        finalString = finalString + util.drawSideBySide(frontString, backString)    
        print(finalString)