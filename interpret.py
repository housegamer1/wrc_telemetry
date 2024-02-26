import util
import dashboard
import raw
import inout
import suspension
import time

timeOfLastFrame = 0
def interpretPacket(data, args):
    #print("data is: " + str(data))

    global timeOfLastFrame
    if timeOfLastFrame == 0:
        timeOfLastFrame = time.time()
    else:
        now = time.time()
        #print("Time since last frame: " + str(round(now - timeOfLastFrame, 2)))
        timeOfLastFrame = now

    bytesAsNumerical = []
    if inout.replayMode == 0:
        bytesAsNumerical = []
        for byte in data:
            bytesAsNumerical.append(byte)
    else:
        bytesAsNumerical = data    

    #print("bytes as numerical: "+  str(bytesAsNumerical))

    #TODO: read actual json config file, determine fields and automatically build packets based on that.
    packet = {}
    if args.config == "custom1":
        packet = interpretCustom1(bytesAsNumerical)
    elif args.config == "custom2":
        packet = interpretCustom2(bytesAsNumerical)

    if packet != {}:
        inout.clearScreen(args)

        if inout.currentScreen == 1:
            dashboard.visualizePacket(packet, False)
        elif inout.currentScreen == 2:
            dashboard.visualizePacket(packet, True)
        elif inout.currentScreen == 3:
            suspension.visualizePacket(packet)
        elif inout.currentScreen == 4:
            raw.printPacket(packet)
    else:
        print("unable to interpret packet")

    if inout.recordingStatus == 1:
        inout.logFrame(bytesAsNumerical)

    
def interpretCustom2(bytesAsNumerical):
    packet = {}

    # vehicle_speed                     4 Bytes float32 in m/s
    packet["vehicle_speed"] = util.resolveSpeedRound(bytesAsNumerical[:4])

    # vehicle_gear_index                1 Byte uint8: 0(N), 1, 2, 3, 4, 5, 6, 7, 10(R)
    packet["vehicle_gear_index"] = util.resolveIntValue(bytesAsNumerical[4:5])

    # vehicle_engine_rpm_current        4 Bytes float32
    packet["vehicle_engine_rpm_current"] = util.resolveFloatValueRound(bytesAsNumerical[5:])

    #print("Packet before interpretation:" + str(bytesAsNumerical))
    return packet

def interpretCustom1(bytesAsNumerical):
    packet = {}

    # packet_uid                        8 Bytes uint64
    packet["packet_uid"] = util.resolveIntValue(bytesAsNumerical[:8])

    # game_total_time                   4 Bytes float32: in seconds
    packet["game_total_time"] = util.resolveFloatValueRound(bytesAsNumerical[8:12])

    # game_delta_time                   4 Bytes float32: in seconds. time since last frame
    packet["game_delta_time"] = util.resolveFloatValue(bytesAsNumerical[12:16])

    # game_frame_count                  8 Bytes uint64
    packet["game_frame_count"] = util.resolveIntValue(bytesAsNumerical[16:24])

    # shiftlights_fraction              4 Bytes float32: 0.0 to 1.0
    packet["shiftlights_fraction"] = util.resolveFloatValue(bytesAsNumerical[24:28]) #dont round

    # shiftlights_rpm_start             4 Bytes float32
    packet["shiftlights_rpm_start"] = util.resolveFloatValueRound(bytesAsNumerical[28:32])

    # shiftlights_rpm_end               4 Bytes float32
    packet["shiftlights_rpm_end"] = util.resolveFloatValueRound(bytesAsNumerical[32:36])
    
    # shiftlights_rpm_valid             1 Byte boolean
    packet["shiftlights_rpm_valid"] = util.resolveBoolean(bytesAsNumerical[36:37])

    # vehicle_gear_index                1 Byte uint8: 0(N), 1, 2, 3, 4, 5, 6, 7, 10(R)
    packet["vehicle_gear_index"] = util.resolveIntValue(bytesAsNumerical[37:38])

    # vehicle_gear_index_neutral        1 Byte uint8: equal to index if neutral
    packet["vehicle_gear_index_neutral"] = util.resolveIntValue(bytesAsNumerical[38:39])

    # vehicle_gear_index_reverse        1 Byte uint8: equal to index if reverse
    packet["vehicle_gear_index_reverse"] = util.resolveIntValue(bytesAsNumerical[39:40])

    # vehicle_gear_maximum              1 Byte uint8: amount of fwd gears
    packet["vehicle_gear_maximum"] = util.resolveIntValue(bytesAsNumerical[40:41])

    # vehicle_speed                     4 Bytes float32: in m/s "gps" speed - no slip
    packet["vehicle_speed"] = util.resolveSpeedRound(bytesAsNumerical[41:45])

    # vehicle_transmission_speed        4 Bytes float32: in m/s "wheel" speed - has slip
    packet["vehicle_transmission_speed"] = util.resolveSpeedRound(bytesAsNumerical[45:49])

    # vehicle_position_x                4 Bytes float32: in m
    packet["vehicle_position_x"] = util.resolveFloatValueRound(bytesAsNumerical[49:53])

    # vehicle_position_y                4 Bytes float32: in m
    packet["vehicle_position_y"] = util.resolveFloatValueRound(bytesAsNumerical[53:57])

    # vehicle_position_z                4 Bytes float32: in m
    packet["vehicle_position_z"] = util.resolveFloatValueRound(bytesAsNumerical[57:61])

    # vehicle_velocity_x                4 Bytes float32: in m/s
    packet["vehicle_velocity_x"] = util.resolveSpeedRound(bytesAsNumerical[61:65])

    # vehicle_velocity_y                4 Bytes float32: in m/s
    packet["vehicle_velocity_y"] = util.resolveSpeedRound(bytesAsNumerical[65:69])

    # vehicle_velocity_z                4 Bytes float32: in m/s
    packet["vehicle_velocity_z"] = util.resolveSpeedRound(bytesAsNumerical[69:73])

    # vehicle_acceleration_x            4 Bytes float32: in m/s²
    packet["vehicle_acceleration_x"] = util.resolveFloatValue(bytesAsNumerical[73:77])

    # vehicle_acceleration_y            4 Bytes float32: in m/s²
    packet["vehicle_acceleration_y"] = util.resolveFloatValue(bytesAsNumerical[77:81])

    # vehicle_acceleration_z            4 Bytes float32: in m/s²
    packet["vehicle_acceleration_z"] = util.resolveFloatValue(bytesAsNumerical[81:85])

    # vehicle_left_direction_x          4 Bytes float32
    packet["vehicle_left_direction_x"] = util.resolveFloatValueRound(bytesAsNumerical[85:89])

    # vehicle_left_direction_y          4 Bytes float32
    packet["vehicle_left_direction_y"] = util.resolveFloatValueRound(bytesAsNumerical[89:93])

    # vehicle_left_direction_z          4 Bytes float32
    packet["vehicle_left_direction_z"] = util.resolveFloatValueRound(bytesAsNumerical[93:97])

    # vehicle_forward_direction_x       4 Bytes float32
    packet["vehicle_forward_direction_x"] = util.resolveFloatValueRound(bytesAsNumerical[97:101])

    # vehicle_forward_direction_y       4 Bytes float32
    packet["vehicle_forward_direction_y"] = util.resolveFloatValueRound(bytesAsNumerical[101:105])

    # vehicle_forward_direction_z       4 Bytes float32
    packet["vehicle_forward_direction_z"] = util.resolveFloatValueRound(bytesAsNumerical[105:109])

    # vehicle_up_direction_x            4 Bytes float32
    packet["vehicle_up_direction_x"] = util.resolveFloatValueRound(bytesAsNumerical[109:113])

    # vehicle_up_direction_y            4 Bytes float32
    packet["vehicle_up_direction_y"] = util.resolveFloatValueRound(bytesAsNumerical[113:117])

    # vehicle_up_direction_z            4 Bytes float32
    packet["vehicle_up_direction_z"] = util.resolveFloatValueRound(bytesAsNumerical[117:121])

    # vehicle_hub_position_bl           4 Bytes float32: in m
    packet["vehicle_hub_position_bl"] = util.resolveFloatValue(bytesAsNumerical[121:125])

    # vehicle_hub_position_br           4 Bytes float32: in m
    packet["vehicle_hub_position_br"] = util.resolveFloatValue(bytesAsNumerical[125:129])

    # vehicle_hub_position_fl           4 Bytes float32: in m
    packet["vehicle_hub_position_fl"] = util.resolveFloatValue(bytesAsNumerical[129:133])

    # vehicle_hub_position_fr           4 Bytes float32: in m
    packet["vehicle_hub_position_fr"] = util.resolveFloatValue(bytesAsNumerical[133:137])

    # vehicle_hub_velocity_bl           4 Bytes float32: in m/s
    packet["vehicle_hub_velocity_bl"] = util.resolveSpeed(bytesAsNumerical[137:141])

    # vehicle_hub_velocity_br           4 Bytes float32: in m/s
    packet["vehicle_hub_velocity_br"] = util.resolveSpeed(bytesAsNumerical[141:145])

    # vehicle_hub_velocity_fl           4 Bytes float32: in m/s
    packet["vehicle_hub_velocity_fl"] = util.resolveSpeed(bytesAsNumerical[145:149])

    # vehicle_hub_velocity_fr           4 Bytes float32: in m/s
    packet["vehicle_hub_velocity_fr"] = util.resolveSpeed(bytesAsNumerical[149:153])

    # vehicle_cp_forward_speed_bl       4 Bytes float32: in m/s
    packet["vehicle_cp_forward_speed_bl"] = util.resolveSpeed(bytesAsNumerical[153:157])

    # vehicle_cp_forward_speed_br       4 Bytes float32: in m/s
    packet["vehicle_cp_forward_speed_br"] = util.resolveSpeed(bytesAsNumerical[157:161])

    # vehicle_cp_forward_speed_fl       4 Bytes float32: in m/s
    packet["vehicle_cp_forward_speed_fl"] = util.resolveSpeed(bytesAsNumerical[161:165])

    # vehicle_cp_forward_speed_fr       4 Bytes float32: in m/s
    packet["vehicle_cp_forward_speed_fr"] = util.resolveSpeed(bytesAsNumerical[165:169])

    # vehicle_brake_temperature_bl      4 Bytes float32: in °C
    packet["vehicle_brake_temperature_bl"] = util.resolveFloatValueRound(bytesAsNumerical[169:173])

    # vehicle_brake_temperature_br      4 Bytes float32: in °C
    packet["vehicle_brake_temperature_br"] = util.resolveFloatValueRound(bytesAsNumerical[173:177])

    # vehicle_brake_temperature_fl      4 Bytes float32: in °C
    packet["vehicle_brake_temperature_fl"] = util.resolveFloatValueRound(bytesAsNumerical[177:181])

    # vehicle_brake_temperature_fr      4 Bytes float32: in °C
    packet["vehicle_brake_temperature_fr"] = util.resolveFloatValueRound(bytesAsNumerical[181:185])

    # vehicle_engine_rpm_max            4 Bytes float32
    packet["vehicle_engine_rpm_max"] = util.resolveFloatValueRound(bytesAsNumerical[185:189])

    # vehicle_engine_rpm_idle           4 Bytes float32
    packet["vehicle_engine_rpm_idle"] = util.resolveFloatValueRound(bytesAsNumerical[189:193])

    # vehicle_engine_rpm_current        4 Bytes float32
    packet["vehicle_engine_rpm_current"] = util.resolveFloatValueRound(bytesAsNumerical[193:197])

    # vehicle_throttle                  4 Bytes float32: 0.0 to 1.0 (after assists)
    packet["vehicle_throttle"] = util.resolveFloatValue(bytesAsNumerical[197:201])

    # vehicle_brake                     4 Bytes float32: 0.0 to 1.0 (after assists)
    packet["vehicle_brake"] = util.resolveFloatValue(bytesAsNumerical[201:205])

    # vehicle_clutch                    4 Bytes float32: 0.0 to 1.0 (after assists)
    packet["vehicle_clutch"] = util.resolveFloatValue(bytesAsNumerical[205:209])

    # vehicle_steering                  4 Bytes float32: -1.0 to 1.0 (after assists)
    packet["vehicle_steering"] = util.resolveFloatValue(bytesAsNumerical[209:213])

    # vehicle_handbrake                 4 Bytes float32: 0.0 - 1.0 (after assists)
    packet["vehicle_handbrake"] = util.resolveFloatValue(bytesAsNumerical[213:217])

    # stage_current_time                4 Bytes float32: in s
    packet["stage_current_time"] = util.resolveFloatValue(bytesAsNumerical[217:221])

    # stage_current_distance            8 Bytes float64: in m
    packet["stage_current_distance"] = util.resolveDoubleValue(bytesAsNumerical[221:229])

    # stage_length                      8 Bytes float64: in m
    packet["stage_length"] = util.resolveDoubleValue(bytesAsNumerical[229:237])

    return packet
