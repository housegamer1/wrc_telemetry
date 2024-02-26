import util

def _visHubPosition(pos):
    height = 20 #lets go from -0.20 to + 0.20. means we jump for every 0.02
    graph = ["\t .\n" for x in range(height)]

    counter = 0
    value = 0.20
    while value > pos:
        value = value - 0.02
        counter = counter + 1

        #check after change
        if value <= pos:
            break

        if counter == height -1:
            break

    
    #replace position in graph
    if counter == 0:
        graph[counter] = "\t||| " + util.setcolor("purple") + "MIN" + util.setcolor("white") +"\n"    
    elif counter == 19:
        graph[counter] = "\t||| " + util.setcolor("purple") + "MAX" + util.setcolor("white") +"\n"    
    else:
        graph[counter] = "\t|||\n"


    returnstring = util.listToString(graph, False)
    return returnstring





def visualizePacket(packet):
    requiredData = []
    requiredData.append("vehicle_hub_position_fl")
    requiredData.append("vehicle_hub_position_fr")
    requiredData.append("vehicle_hub_position_bl")
    requiredData.append("vehicle_hub_position_br")
    requiredData.append("vehicle_hub_velocity_fl")
    requiredData.append("vehicle_hub_velocity_fr")
    requiredData.append("vehicle_hub_velocity_bl")
    requiredData.append("vehicle_hub_velocity_br")
    

    for needed in requiredData:
        if needed not in packet:
            print("required data not in packet:" + needed)
            return
        
    posFl = packet["vehicle_hub_position_fl"]
    posFr = packet["vehicle_hub_position_fr"]
    posBl = packet["vehicle_hub_position_bl"]
    posBr = packet["vehicle_hub_position_br"]

    velFl = packet["vehicle_hub_velocity_fl"]
    velFr = packet["vehicle_hub_velocity_fr"]
    velBl = packet["vehicle_hub_velocity_bl"]
    velBr = packet["vehicle_hub_velocity_br"]

    finalString = ""
    posFlString = "Front Left\n" + _visHubPosition(packet["vehicle_hub_position_fl"])
    posFrString = "Front Right\n" + _visHubPosition(packet["vehicle_hub_position_fr"])
    posBlString = "Back Left\n" + _visHubPosition(packet["vehicle_hub_position_bl"])
    posBrString = "Back Right\n" + _visHubPosition(packet["vehicle_hub_position_br"])

    frontString = util.drawSideBySide(posFlString, posFrString)
    backString = util.drawSideBySide(posBlString, posBrString)


    finalString = finalString + util.drawSideBySide(frontString, backString)

    # posString = ">>>   posFl: " + str(posFl) + "\t"
    # posString = posString + "posFr: " + str(posFr) + "\n"
    # posString = posString + ">>>   posBl: " + str(posBl) + "\t"
    # posString = posString + "posBr: " + str(posBr) + "\n"

    # velString = ">>>   velFl: " + str(velFl) + "\t"
    # velString = velString + "velFr: " + str(velFr) + "\n"
    # velString = velString + ">>>   velBl: " + str(velBl) + "\t"
    # velString = velString + "velBr: " + str(velBr) + "\n"

    # bothString = util.drawSideBySide(posString, velString)
    
    print(finalString)