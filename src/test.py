import dashboard
import inout 
import suspension
import util

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
        "vehicle_hub_position_br" : -0.12
    }

    print("=== Hub pos test ===")
    suspension.visualizePacket(packet)
    print("=== Hub pos test end ===")


def testResolveId():
    print("=== Hub pos test ===")
    print(util.resolveId(70, "vehicles"))
    print("=== Hub pos test end ===")


def testCatalogue():
    print("=== Catalogue Test ===")

    inout.updateSuspensionCatalogue(32, "Loose", -3, 8)
    inout.updateSuspensionCatalogue(32, "Tarmac", -6, 4)
    inout.updateSuspensionCatalogue(65, "Tarmac", -6, 4)
    currentCatalogue = inout.getSuspensionCatalogue()
    print("Catalogue is: " + str(currentCatalogue))
    print("=== Catalogue Test end ===")

if __name__ == "__main__":
    #testSteering()
    #testAccel()
    #testMenu()
    #testHubPos()
    #testResolveId()
    testCatalogue()