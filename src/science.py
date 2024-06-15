import time
import util
import inout

accelStartMeasureTime = 0
measuredTimes = []
def measureZeroToOnehundred(packet):
    global measuredTimes
    global accelStartMeasureTime
    measureTimeString = ""
    if "vehicle_speed" in packet:
            

            if accelStartMeasureTime != 0:
                measureTimeString = measureTimeString + "Ready to measure 0-100!" + str(packet["vehicle_speed"]) + "\n"

            if packet["vehicle_speed"] == 0:
                accelStartMeasureTime = time.time()
            elif packet["vehicle_speed"] >= 100 and accelStartMeasureTime != 0:
                measuredTimes.append(time.time() - accelStartMeasureTime)
                accelStartMeasureTime = 0

    if measuredTimes != []:
        measureTimeString = measureTimeString + ">>>   Measured 0-100 Times:\n"
        for measure in measuredTimes:
            measureTimeString  = measureTimeString + ">>>   " + str(measure) + "\n"
    
    return measureTimeString


powerband = {}
def measureGforce(packet):
    #since the acceleration isnt bound to the car sadly, we will just add the vectors together
    #alternative approach: we could see how many gps kmh are gained in an rpm window.
    #additional benefit of the alternative approach: bumps in the road at high speeds should 
    #not interfere as much with the gathered data.
    #for now, lets try g force.

    #in order to actually measure the engine, we want 0 steering, as that would influence sideways g forces,
    #full throttle, and we need to keep this data for every gear, otherwise it is not compareable.
    #if the player changes the gearing or hits a abump or obstacle, this data will sadly become inaccurate.
    #therefore i will (probably) not create a power curve catalogue, and instead only show the current power curve.
    global powerband

    distance = packet["stage_current_distance"]
    if distance == 0.0:
        powerband = {}

    #these are m/s² so convert to g
    accelX = round(packet["vehicle_acceleration_x"] / 9.81, 1)
    accelZ = round(packet["vehicle_acceleration_z"] / 9.81, 1)
    accelCombined = abs(accelX + accelZ)
    rpmAccuracy = 100
    rpm = util.roundToNearest(packet["vehicle_engine_rpm_current"], rpmAccuracy)
    maxrpm = util.roundToNearest(packet["vehicle_engine_rpm_max"], rpmAccuracy)
    throttle = packet["vehicle_throttle"]
    steering = packet["vehicle_steering"]
    brake = packet["vehicle_brake"]
    currentGear = packet["vehicle_gear_index"]
    gpsspeed = packet["vehicle_speed"]

    #going straight and flat out.
    if brake == 0.0 and  throttle == 1.0 and steering <= 0.1 and steering >= -0.1 and currentGear != 0 and gpsspeed > 15:

        gear = {}
        if currentGear in powerband:
            gear = powerband[currentGear]
            if not rpm in gear:
                gear[rpm] = accelCombined
                powerband[currentGear] = gear
             
        else:
            gear[rpm] = accelCombined
            powerband[currentGear] = gear

    gforceString = "Gear: " + str(currentGear) + ", G: " + str(accelCombined) + "\n"
    if powerband != {}:
        gforceString = gforceString + visualizeGforce(maxrpm,rpmAccuracy, currentGear)

    return gforceString

def visualizeGforce(maxrpm, rpmAccuracy, currentGear):
    global powerband

    rpmRange = round(maxrpm / rpmAccuracy)

    maxGShown = 1.5
    yAxis = round(maxGShown * 10)
   
    graph = [[" " for x in range(rpmRange)] for y in range(yAxis)] # draw empty graph

    for entry in range(rpmRange): # draw graph border
        graph[yAxis -1][entry -1] = "_"
        graph[0][entry -1] = "_"
 
    if currentGear in powerband:
        gear = powerband[currentGear]
        for rpm in gear:
            rpmColumn = util.clamp(round(rpm / rpmAccuracy), 0, rpmRange -1)
            gLevel = util.clamp(round(gear[rpm] *10), 0, yAxis -1)

            correctedGLevel = util.clamp(yAxis - gLevel, 0, yAxis -1)  #flip the graph upside down

            #print("graph[" + str(gLevel) + "][" + str(rpmColumn) + "]")
            graph[correctedGLevel][rpmColumn] = "X"


    returnstring = ""
    for row in graph:
        returnstring = returnstring + "\t\t" + util.listToString(row, False) + "\n"
    returnstring = returnstring + "\n"

    return returnstring



def printPacket(packet):
    measureTimeString = measureZeroToOnehundred(packet)
    gforceString = measureGforce(packet)

    #print("Measure time string: " + measureTimeString)
    #print("gforce string: " + gforceString)
    #print function results, ideally side by side
    printString = ""


    if inout.togglePowerband:
        printString = ">>>   Press (T) to toggle 0-100 times\n"
        printString = printString + gforceString
    else:
        printString = ">>>   Press (T) to toggle powerband\n"
        printString = printString + measureTimeString

    print(printString)

    

        