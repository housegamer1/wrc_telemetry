import os
import util

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

def _visSteering(data):
    returnstring = "["

    if data > 0.0: #right steer
        returnstring = returnstring + "     "
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

    elif data < 0.0: #left steer
        counter = -1.0
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
        returnstring = returnstring + "     "
    
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
    

def visualizePacket(packet, args):
    util.clearScreen(args.isgitbash)

    if args.isgitbash:
        print('\033[?25l', end="")  #hide cursor to prevent flashing. idk why this ansi code works but not clear screen...
    
    #pick pedals, steering, rpm, speed, time, distance
    printstring = ">>>   Throttle:\t\t" + _visPedal(packet["vehicle_throttle"], "green") + "\n"
    printstring = printstring + ">>>   Brake:\t\t" + _visPedal(packet["vehicle_brake"], "red") + "\n"
    printstring = printstring + ">>>   Clutch:\t\t" + _visPedal(packet["vehicle_clutch"], "white") + "\n"
    printstring = printstring + ">>>   Handbrake:\t" + _visPedal(packet["vehicle_handbrake"], "red") + "\n\n"
    
    printstring = printstring + ">>>   Steering:\t\t" + _visSteering(packet["vehicle_steering"]) + "\n\n"

    printstring = printstring + ">>>   Gear:\t\t" + _visGear(packet) + "\n"
    printstring = printstring + ">>>   RPM:\t\t" + _visRpm(packet) + "\n"

    transspeed = packet["vehicle_transmission_speed"]
    gpsspeed = packet["vehicle_speed"]

    slip = ""
    if transspeed > gpsspeed * 1.2: #should roughly take care of the losses
        slip = _setcolor("purple") + "**SLIP**"+ _setcolor("white") 
    elif transspeed < gpsspeed * 0.5: 
        slip = _setcolor("purple") + "**LOCKUP**"+ _setcolor("white") 

    printstring = printstring + ">>>   Trans Speed:\t" + str(packet["vehicle_transmission_speed"]) + " Km/h  " + slip + "\n"
    printstring = printstring + ">>>   Gps Speed:\t" + str(packet["vehicle_speed"]) + " Km/h\n"

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