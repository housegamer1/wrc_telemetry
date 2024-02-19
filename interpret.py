import struct
import util

def interpretPacket(data):

    #packet_uid: 8 Bytes: [Least significant byte, ..., ..., ..., ..., ..., ..., Most significant byte]
    #game_total_time: 4 Bytes float32 in s
    #vehicle_gear_index: 1 Byte uint8: 0(N), 1, 2, 3, 4, 5, 6, 7, 10(R)
    #vehicle_speed 4 Bytes float32 in m/s
    #vehicle_engine_rpm_current 4 Bytes float32
    
    bytesAsNumerical = []
    for byte in data:
        bytesAsNumerical.append(byte)

    vehicleSpeed = resolveVehicleSpeed(bytesAsNumerical[:4])
    vehicleGear = resolveVehicleGear(bytesAsNumerical[4:5])
    vehicleRpm = resolveRpm(bytesAsNumerical[5:])

    #print("Packet:" + str(bytesAsNumerical))
    print(">>>    Speed: "  + str(vehicleSpeed) + "  Gear: "  + str(vehicleGear) + "  Rpm: "  + str(vehicleRpm) + "            ", end="\r")


def resolveVehicleSpeed(byteValues):
    asBytes = bytes(byteValues)
    asMps = struct.unpack("f", asBytes)[0] # in m/s
    asKmh = util.mpsToKmh(asMps)

    return round(asKmh)

def resolveVehicleGear(byteValues):
    asBytes = bytes(byteValues)
    asInt = int.from_bytes(asBytes, byteorder="little")

    return asInt
    
def resolveRpm(byteValues):
    asBytes = bytes(byteValues)
    asRpm = struct.unpack("f", asBytes)[0]

    return round(asRpm)