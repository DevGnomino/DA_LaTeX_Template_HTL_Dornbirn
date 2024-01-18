import math

def standard(sensors, additional_info):
    return sensors[0].get_data_from_modbus()

def calc_wrg(sensors, additional_info):
    exhaust_air = sensors[0].get_data_from_modbus()  # Abluft
    outgoing_air = sensors[1].get_data_from_modbus()  # Fortluft
    outside_air = sensors[2].get_data_from_modbus()  # Außenluft

    wrg = (exhaust_air - outgoing_air) / (exhaust_air - outside_air)

    return str(round(wrg)) + " %"

def eng_status(sensors, additional_info):
    status = sensors[0].get_data_from_modbus()
    binary_status = bin(status)
    error_string = ""
    counter = 0
    for s in reversed(binary_status):
        counter += 1
        if s == "1":
            if counter == 1:
                error_string += "PHA "
            if counter == 3:
                error_string += "TFE "
            if counter == 4:
                error_string += "SKF "
            if counter == 5:
                error_string += "FB "
            if counter == 6:
                error_string += "TFM "
            if counter == 7:
                error_string += "HLL "
            if counter == 8:
                error_string += "BLK "
            if counter == 9:
                error_string += "n_Limit "
            if counter == 11:
                error_string += "RL_Cal "
            if counter == 13:
                error_string += "UzLow "

            # This should never occur:
            if counter == 2 or counter == 10 or counter == 12 or counter > 13:
                error_string += "Unbekannter Fehler"

    if error_string == "":
        error_string = "Kein Fehler"

    return error_string

def calc_volume(sensors, additional_info):
    sensor_value = sensors[0].get_data_from_modbus()

    # when the fan isn't spinning it doesn't move air, but the pressure sensor still detects a pressure difference
    # so: if the pressure difference is to small the moved volume is just assumed to be 0
    if sensor_value <= 5:
        return_str = "0 m³/h"
    else:
        return_str = str(round(math.sqrt(sensor_value) * additional_info["k-faktor"])) + " m³/h"

    return return_str

def calc_rpm(sensors, additional_info):
    max_value = sensors[1].get_data_from_modbus()
    rpm_value = (sensors[0].get_data_from_modbus() / 64000) * max_value
    ratio = rpm_value / max_value * 100.0
    return str(round(ratio, 1)) + " %"

def calc_power(sensors, additional_info):
    byte_value = sensors[0].get_data_from_modbus()
    Uz_value = sensors[1].get_data_from_modbus() / 1000
    Iz_value = sensors[2].get_data_from_modbus() / 1000
    print(byte_value, Uz_value, Iz_value)
    power = (byte_value / 65536) * Uz_value * 20 * Iz_value * 2
    return str(round(power, 1)) + " W"

def flap_position(sensors, additional_info):
    flap_mv = sensors[0].get_data_from_modbus()
    flap_pos = flap_mv / 10500 * 100
    return str(round(flap_pos)) + " %"

def relay_position(sensors, additional_info):
    relay_mv = sensors[0].get_data_from_modbus()
    if relay_mv < additional_info["switching_voltage"]:
        return "Geschlossen"
    else:
        return "Offen"
