import socket
import time
import interpret
import argparse
import inout
import util
import suspension

def connectToServer(args):

    print("Ip is " + args.ip + ":" + str(args.port))
    print("")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.1) #if nothing received after .1 sec, jump to socket.error catch block
    sock.bind((args.ip, args.port))

    interpTime = 0

    #how long to wait until the next packet is handled.
    #if this is smaller than the packet handling time taken, the programm will be behind what is happening in the game.
    #the larger this number, the less responsive the ui will be.
    packetHandlingDelay = 0.06
    latestPacket = {}
    lastPackageUsedToUpdate = None

    try:
        while True:
            if inout.replayMode == 0:
                try:
                    data = sock.recvfrom(512)[0] #TODO: figure out dynamic size?
                    recvTime = time.time()

                    #try not to interpret every frame.
                    #if the whole function sleeps, the sleep will just create delay in the information
                    #so instead we keep receiving to pop from the socket but we do nothing with some of the packets
                    if (recvTime - interpTime) > packetHandlingDelay:
                        t1 = time.time()
                        packet = interpret.interpretPacket(data, args)
                        if packet != {}:
                            latestPacket = packet.copy()

                        t2 = time.time()

                        timeToHandlePacket = round(t2 - t1, 2)

                        if timeToHandlePacket > packetHandlingDelay:
                            print("interpreting packet took too long, cpu not sleeping!")
                        #print("Packet took: " + str(timeToHandlePacket))
                        interpTime = recvTime

                except socket.error:
                    inout.clearScreen(args)
                    #when we lose packets, it might be the end of the stage (or game paused), so write out the data we gathered.
                    suspension.prepCatalogueUpdate()

                    if latestPacket != lastPackageUsedToUpdate:
                        inout.updatePBTable(latestPacket)
                        lastPackageUsedToUpdate = latestPacket.copy()

                    print(">>>    No packets received, sleeping")
                    #print("\nLatest Packet:\n" + str(latestPacket))
                    time.sleep(0.25)

            else:
                inout.showLoadMenu(args)
                time.sleep(0.1)

    except KeyboardInterrupt:
        util.quit(args)


def main():
    parser = argparse.ArgumentParser(prog='wrc_telemetry', description='Read UDP telemetry for EA Sports WRC')
    parser.add_argument("-c", "--config", help="custom1 or custom2 or customX. default custom1", default="custom1", required=False)
    parser.add_argument("-i", "--ip", help="override the used ip. default 127.0.0.1", default="127.0.0.1", required=False)
    parser.add_argument("-p", "--port", help="override the used port. default 20777", type=int, default=20777,required=False)
    parser.add_argument("-g", "--isgitbash", help="uses clear to clear screen to avoid flicker", default=False,required=False, action="store_true")
    args = parser.parse_args()

    print("Args: " + str(args))
    connectToServer(args)

if __name__ == "__main__":
    main()