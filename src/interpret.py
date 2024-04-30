import util
import dashboard
import raw
import inout
import suspension
import time
import science

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
    #print("Number of exported fields: "+  str(len(bytesAsNumerical)))

    #TODO: read actual json config file, determine fields and automatically build packets based on that.
    t1 = time.time()
    packet = {}
    if args.config == "custom1":
        packet = interpretCustom1(bytesAsNumerical, False)
    if args.config == "custom1_mod":
        packet = interpretCustom1(bytesAsNumerical, True) #too lazy to make dynamic config loading just yet
    elif args.config == "custom2":
        packet = interpretCustom2(bytesAsNumerical)

    t2 = time.time()
    t4 = 0
    if packet != {}:
        inout.clearScreen(args)
        t4 = time.time()

        if inout.currentScreen == 1:
            dashboard.visualizePacket(packet, False)
        elif inout.currentScreen == 2:
            dashboard.visualizePacket(packet, True)
        elif inout.currentScreen == 3:
            suspension.visualizePacket(packet, False)
        elif inout.currentScreen == 4:
            raw.printPacket(packet)
        elif inout.currentScreen == 5:
            science.printPacket(packet)

        if inout.currentScreen != 3:
            suspension.visualizePacket(packet, True) #run the suspension code but hide the visuals, so we can record min and max values for our catalogue
    else:
        print("unable to interpret packet")

    t3 = time.time()

    timeToInterpret = round(t2-t1, 2)
    timeToDraw = round(t3-t2, 2)
    timeToClear = round(t4-t2, 2)

    #print("Time to interpret: " + str(timeToInterpret))
    #print("Time to draw: " + str(timeToDraw))
    #print("Time to clear screen: " + str(timeToClear))


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

def interpretCustom1(bytesAsNumerical, modifiedCustom1):
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

    if modifiedCustom1:
        #vehicle_id                     2 Bytes uint16
        packet["vehicle_id"] = util.resolveIntValue(bytesAsNumerical[237:239])

        #vehicle_class_id               2 Bytes uint16
        packet["vehicle_class_id"] = util.resolveIntValue(bytesAsNumerical[239:241])

        #vehicle_manufacturer_id        2 Bytes uint16
        packet["vehicle_manufacturer_id"] = util.resolveIntValue(bytesAsNumerical[241:243])

        #location_id                    2 Bytes uint16
        packet["location_id"] = util.resolveIntValue(bytesAsNumerical[243:245])

        #route_id                       2 Bytes uint16
        packet["route_id"] = util.resolveIntValue(bytesAsNumerical[245:247])


        #Below is from update 1.7.0
        #Loading a replay from an older version would crash here, so we need to do a size check
        if len(bytesAsNumerical) > 247:
        
            #stage_shakedown                1 Byte boolean
            packet["stage_shakedown"] = util.resolveBoolean(bytesAsNumerical[247:248])


        #Below is from update 1.8.0
        #Loading a replay from an older version would crash here, so we need to do a size check
        if len(bytesAsNumerical) > 270:

            #game_mode                      1 Byte uint8: id
            packet["game_mode"] = util.resolveIntValue(bytesAsNumerical[248:249])

            #stage_previous_split_time      4 Bytes float32: in s
            packet["stage_previous_split_time"] = util.resolveFloatValue(bytesAsNumerical[249:253])
            
            #stage_progress                 4 Bytes float32: in % 0-1        
            packet["stage_progress"] = util.resolveFloatValue(bytesAsNumerical[253:257])

            #stage_result_time              4 Bytes float32: in s
            packet["stage_result_time"] = util.resolveFloatValue(bytesAsNumerical[257:261])

            #stage_result_time_penalty      4 Bytes float32: in s
            packet["stage_result_time_penalty"] = util.resolveFloatValue(bytesAsNumerical[261:265])

            #stage_result_status            1 Byte uint8: id
            packet["stage_result_status"] = util.resolveIntValue(bytesAsNumerical[265:266])

            #vehicle_cluster_abs            1 Byte boolean
            packet["vehicle_cluster_abs"] = util.resolveBoolean(bytesAsNumerical[266:267])

            #vehicle_tyre_state_bl          1 Byte uint8: id
            packet["vehicle_tyre_state_bl"] = util.resolveIntValue(bytesAsNumerical[267:268])

            #vehicle_tyre_state_br          1 Byte uint8: id
            packet["vehicle_tyre_state_br"] = util.resolveIntValue(bytesAsNumerical[268:269])
            
            #vehicle_tyre_state_fl          1 Byte uint8: id
            packet["vehicle_tyre_state_fl"] = util.resolveIntValue(bytesAsNumerical[269:270])

            #vehicle_tyre_state_fr          1 Byte uint8: id
            packet["vehicle_tyre_state_fr"] = util.resolveIntValue(bytesAsNumerical[270:271])

    return packet
