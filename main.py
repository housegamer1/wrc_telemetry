import socket
import time
import interpret
import argparse
import os

def connectToServer(args):

    print("Ip is " + args.ip + ":" + str(args.port))
    print("")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.25) #if nothing received after .25 sec, jump to socket.error catch block
    sock.bind((args.ip, args.port))

    interpTime = 0
    try:
        while True:
            try:
                data = sock.recvfrom(256)[0] #TODO: figure out dynamic size?
                recvTime = time.time()
                
                #try not to interpret every frame.
                #if the whole function sleeps, the sleep will just create delay in the information
                #so instead we keep receiving to pop from the socket but we do nothing with some of the packets
                if (recvTime - interpTime) > 0.1:
                    interpret.interpretPacket(data, args.config)
                    interpTime = recvTime

            except socket.error:
                os.system("clear")
                print('\033[?25l', end="") #hide cursor to prevent flashing. idk why this ansi code works but not clear screen...
                print(">>>    No packets received, sleeping")
                time.sleep(0.25)
    except KeyboardInterrupt:
        print("")
        print('\033[?25h', end="") #bring cursor back
        print("Quitting")

def main():
    parser = argparse.ArgumentParser(prog='wrc_telemetry', description='Read UDP telemetry for EA Sports WRC')
    parser.add_argument("-c", "--config", help="custom1 or custom2 or customX. default custom1", default="custom1", required=False)
    parser.add_argument("-i", "--ip", help="override the used ip. default 127.0.0.1", default="127.0.0.1", required=False)
    parser.add_argument("-p", "--port", help="override the used port. default 20777", type=int, default=20777,required=False)
    args = parser.parse_args()

    connectToServer(args)

if __name__ == "__main__":
    main()