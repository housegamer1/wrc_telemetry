import socket
import time
import interpret

def connectToServer(server):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.25)
    sock.bind((server["ip"], server["port"]))

    interpTime = 0
    try:
        while True:
            try:
                data = sock.recvfrom(237)[0]
                recvTime = time.time()
                
                #try not to interpret every frame.
                #if the whole function sleeps, the sleep will just create delay in the information
                if (recvTime - interpTime) > 0.1:
                    interpret.interpretPacket(data)
                    interpTime = recvTime

            except socket.error:
                print(">>>    No packets received, sleeping          ", end="\r")
                time.sleep(0.25) #No packets received, sleep a bit
    except KeyboardInterrupt:
        print("")
        print("Quitting")

def main():
    #EA Sports WRC. Works after enabling packages in the json
    server = {
        "ip": "127.0.0.1",
        "port": 20777
    } 

    #Assetto Corsa. Doesnt work, as the game already binds this port??
    #server = {
    #    "ip": "0.0.0.0",
    #    "port": 9996
    #} 
    
    print("Ip is " + server["ip"] + ":" + str(server["port"]))
    print("")
    connectToServer(server)

if __name__ == "__main__":
    main()