def packetToString(packet):
    printstring = ">>>   "
    count = 0
    for field in packet:  
        count = count + 1
        printstring = printstring + str(field) + ": " + str(packet[field]) + " | "
        if count == 3:
            printstring = printstring + "\n>>>   "
            count = 0
    return printstring

def printPacket(packet):
    stringpacket = packetToString(packet)
    print(stringpacket)