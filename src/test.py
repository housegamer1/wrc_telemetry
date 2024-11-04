import dashboard
import inout 
import suspension
import util
import interpret

# not real testing okay, cba to do that.
# just a helper to analyse certain issues


def testSteering():
    print("=== Steering test ===")
    print(dashboard._visSteering(1.0) + " 1.0")
    print(dashboard._visSteering(0.9) + " 0.9")
    print(dashboard._visSteering(0.8) + " 0.8")
    print(dashboard._visSteering(0.7) + " 0.7")
    print(dashboard._visSteering(0.6) + " 0.6")
    print(dashboard._visSteering(0.5) + " 0.5")
    print(dashboard._visSteering(0.4) + " 0.4")
    print(dashboard._visSteering(0.3) + " 0.3")
    print(dashboard._visSteering(0.2) + " 0.2")
    print(dashboard._visSteering(0.1) + " 0.1")
    print(dashboard._visSteering(0.0) + " 0.0")
    print(dashboard._visSteering(-0.0) + " -0.0")
    print(dashboard._visSteering(-0.1) + " -0.1")
    print(dashboard._visSteering(-0.2) + " -0.2")
    print(dashboard._visSteering(-0.3) + " -0.3")
    print(dashboard._visSteering(-0.4) + " -0.4")
    print(dashboard._visSteering(-0.5) + " -0.5")
    print(dashboard._visSteering(-0.6) + " -0.6")
    print(dashboard._visSteering(-0.7) + " -0.7")
    print(dashboard._visSteering(-0.8) + " -0.8")
    print(dashboard._visSteering(-0.9) + " -0.9")
    print(dashboard._visSteering(-1.0) + " -1.0")
    print("=== Steering test part 2===")
    print(dashboard._visSteering(-0.01) + " -0.01")
    print(dashboard._visSteering(-0.11) + " -0.11")
    print(dashboard._visSteering(-0.21) + " -0.21")
    print(dashboard._visSteering(-0.31) + " -0.31")
    print(dashboard._visSteering(-0.41) + " -0.41")
    print(dashboard._visSteering(-0.51) + " -0.51")
    print(dashboard._visSteering(-0.61) + " -0.61")
    print(dashboard._visSteering(-0.71) + " -0.71")
    print(dashboard._visSteering(-0.81) + " -0.81")
    print(dashboard._visSteering(-0.91) + " -0.91")
    print(dashboard._visSteering(-0.99) + " -0.99")
    print(dashboard._visSteering(0.01) + " 0.01")
    print(dashboard._visSteering(0.11) + " 0.11")
    print(dashboard._visSteering(0.21) + " 0.21")
    print(dashboard._visSteering(0.31) + " 0.31")
    print(dashboard._visSteering(0.41) + " 0.41")
    print(dashboard._visSteering(0.51) + " 0.51")
    print(dashboard._visSteering(0.61) + " 0.61")
    print(dashboard._visSteering(0.71) + " 0.71")
    print(dashboard._visSteering(0.81) + " 0.81")
    print(dashboard._visSteering(0.91) + " 0.91")
    print(dashboard._visSteering(0.99) + " 0.99")

    print("=== Steering test end ===")

def testAccel():
    print("=== Accelerometer test ===")
    print(dashboard._visAccel(0,0,0))
    print(dashboard._visAccel(10,0,0))
    print(dashboard._visAccel(20,0,0))
    print(dashboard._visAccel(30,0,0))
    print(dashboard._visAccel(0,10,0))
    print(dashboard._visAccel(0,20,0))
    print(dashboard._visAccel(0,30,0))
    print(dashboard._visAccel(10,10,0))
    print(dashboard._visAccel(20,20,0))
    print(dashboard._visAccel(30,30,0))
    print("=== Accelerometer test end ===")

def testMenu():
    class Arg():
        pass
    args = Arg()
    args.isgitbash = True

    while True:
        inout.clearScreen(args)

def testHubPos():

    #need this for ansi colors
    class Arg():
        pass
    args = Arg()
    args.isgitbash = True
    inout.clearScreen(args)

    packet = {
        "vehicle_hub_position_fl" : 0.0,
        "vehicle_hub_position_fr" : 0.2,
        "vehicle_hub_position_bl" : -0.19,
        "vehicle_hub_position_br" : -0.12,
        "vehicle_id" :  106,
        "location_id" : 13,
        "stage_current_distance": 0
    }

    print("=== Hub pos test ===")
    suspension.visualizePacket(packet, False)
    print("=== Hub pos test end ===")


def testResolveId():
    print("=== Hub pos test ===")
    print(util.resolveId(70, "vehicles"))
    print("=== Hub pos test end ===")


def testCatalogue():
    print("=== Catalogue Test ===")

    inout.updateSuspensionCatalogue(32, "Loose", -3, 8, 0, 12)
    inout.updateSuspensionCatalogue(32, "Tarmac", -6, 4, 3, 5)
    inout.updateSuspensionCatalogue(65, "Tarmac", -6, 4, 6 ,1)
    inout.updateSuspensionCatalogue(4, "Loose", 0, 4, 0 ,0)
    currentCatalogue = inout.getSuspensionCatalogue()
    print("Catalogue is: " + str(currentCatalogue))
    print("=== Catalogue Test end ===")


def testTireStatus():

    #need this for ansi colors
    class Arg():
        pass
    args = Arg()
    args.isgitbash = True
    inout.clearScreen(args)

    packet = {
        "vehicle_tyre_state_bl" : 0,
        "vehicle_tyre_state_br" : 1,
        "vehicle_tyre_state_fl" : 2,
        "vehicle_tyre_state_fr" : 3,
        "vehicle_id" :  106,
        "location_id" : 13,
        "stage_current_distance": 0
    }

    print("=== Hub pos test ===")
    print(dashboard._visTireState(packet))
    print("=== Hub pos test end ===")

def testTimeDB():
    rawpacket = [172, 68, 0, 0, 0, 0, 0, 0, 9, 149, 20, 68, 137, 136, 136, 60, 251, 201, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 54, 216, 241, 69, 29, 188, 0, 70, 1, 3, 0, 10, 5, 125, 105, 176, 65, 227, 250, 127, 63, 55, 228, 188, 68, 58, 20, 216, 194, 70, 224, 43, 197, 40, 41, 174, 65, 165, 120, 133, 191, 127, 156, 86, 64, 207, 34, 95, 193, 104, 46, 52, 64, 152, 198, 145, 191, 17, 82, 46, 191, 90, 92, 7, 62, 69, 102, 56, 191, 121, 206, 57, 63, 76, 208, 23, 188, 6, 22, 48, 191, 148, 225, 199, 61, 14, 190, 125, 63, 205, 145, 183, 61, 165, 121, 10, 190, 27, 157, 184, 189, 38, 62, 119, 189, 161, 71, 165, 188, 5, 99, 102, 190, 186, 63, 164, 61, 131, 54, 136, 62, 32, 29, 228, 189, 0, 0, 0, 0, 37, 79, 2, 64, 0, 0, 0, 0, 67, 233, 1, 64, 50, 47, 117, 67, 33, 2, 146, 67, 158, 160, 127, 67, 9, 82, 140, 67, 31, 208, 4, 70, 32, 160, 12, 69, 55, 228, 5, 69, 0, 0, 0, 0, 0, 0, 128, 63, 0, 0, 128, 63, 0, 0, 0, 0, 0, 0, 0, 0, 0, 192, 23, 67, 88, 225, 86, 138, 95, 138, 177, 64, 0, 0, 0, 32, 146, 27, 177, 64, 104, 0, 19, 0, 6, 0, 27, 0, 105, 1, 0, 0, 182, 243, 233, 65, 0, 0, 0, 0, 0, 57, 58, 131, 63, 133, 235, 20, 67, 0, 0, 32, 65, 1]
    packet = interpret.interpretCustom1(rawpacket, True)

    inout.updatePBTable(packet)

if __name__ == "__main__":
    #testSteering()
    #testAccel()
    #testMenu()
    #testHubPos()
    #testResolveId()
    #testCatalogue() #dont call unless you made a backup of suspensionCatalogue.json, will introduce fake values 
    #testTireStatus()
    testTimeDB()