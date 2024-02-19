import socket
import struct
import time

def interpretPacket(data):

    #packet_uid: 8 Bytes: [Least significant byte, ..., ..., ..., ..., ..., ..., Most significant byte]
    #game_total_time: 4 Bytes float32 in s
    #vehicle_gear_index: 1 Byte uint8: 0(N), 1, 2, 3, 4, 5, 6, 7, 10(R)
    #vehicle_speed 4 Bytes float32 in m/s
    #vehicle_engine_rpm_current 4 Bytes float32
    
    bytesAsNumerical = []
    for byte in data:
        bytesAsNumerical.append(byte)

    vehicleSpeed = round((struct.unpack("f", bytes(bytesAsNumerical[:4]))[0]  * 3.6))
    vehicleGear = int.from_bytes(bytes(bytesAsNumerical[4:5]), byteorder="little")
    vehicleRpm = round(struct.unpack("f", bytes(bytesAsNumerical[5:]))[0])

    #print("Packet:" + str(bytesAsNumerical))
    print("    Speed: "  + str(vehicleSpeed) + "  Gear: "  + str(vehicleGear) + "  Rpm: "  + str(vehicleRpm) + "            ", end="\r")

def connectToServer(server):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((server["ip"], server["port"]))

    while True:
        data = sock.recvfrom(32)[0]
        interpretPacket(data)
        #time.sleep(0.1)

def main():
    server = {
        "ip": "127.0.0.1",
        "port": 20777
    } #EA Sports Wrc. Works after enabling packages in the json

    #server = {
    #    "ip": "0.0.0.0",
    #    "port": 9996
    #} #Assetto Corsa. Doesnt work, as the game already binds this port??
    
    print("Ip is " + str(server))
    print("")
    connectToServer(server)

if __name__ == "__main__":
    main()