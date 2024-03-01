import time

accelStartMeasureTime = 0
measuredTimes = []
def printPacket(packet):
    if "vehicle_speed" in packet:
        global accelStartMeasureTime

        if accelStartMeasureTime != 0:
            print("Ready to measure 0-100!" + str(packet["vehicle_speed"]))

        if packet["vehicle_speed"] == 0:
            accelStartMeasureTime = time.time()
        elif packet["vehicle_speed"] >= 100 and accelStartMeasureTime != 0:
            measuredTimes.append(time.time() - accelStartMeasureTime)
            accelStartMeasureTime = 0

    if measuredTimes != []:
        print(">>>   Measured 0-100 Times:\n")
        for measure in measuredTimes:
            print(">>>   " + str(measure))
        