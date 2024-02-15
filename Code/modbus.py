import minimalmodbus as minmb
import customtkinter as ctk
import sys
import os
import time
from threading import Thread
import math
import json
import modbus_functions

CONFIG_PATH = '/home/pi/Documents/RLT_Config/'
DEVICES_CONFIG_PATH = '/home/pi/Documents/RLT_Config/devices/'

class Sensor():
    def __init__(self, baud_rate, mb_address, parity, stop_bits, scaling, register,
                 function_code, zero_based):
        self.scaling = scaling
        if zero_based:
            self.register = register
        else:
            self.register = register - 1
        self.function_code = function_code

        # Mit USB Connector auf Linux       /dev/ttyUSB0
        # Mit USB Connector auf Windows     COM4
        # Über TX (8) und RX (10) Pins      /dev/ttyAMA0
        self.instrument = minmb.Instrument('/dev/ttyAMA0',
                                       mb_address)  # Make an "instrument" object called sensor (port name, slave address (in decimal))
        self.instrument.serial.baudrate = baud_rate
        self.instrument.serial.bytesize = 8  # Number of data bits to be requested

        if parity == "even":  # Parity Setting can be ODD, EVEN or NONE
            self.instrument.serial.parity = minmb.serial.PARITY_EVEN
        elif parity == "odd":
            self.instrument.serial.parity = minmb.serial.PARITY_ODD
        else:
            self.instrument.serial.parity = minmb.serial.PARITY_NONE

        self.instrument.serial.stopbits = stop_bits  # Number of stop bits
        self.instrument.serial.timeout = 0.5  # Timeout time in seconds
        self.instrument.mode = minmb.MODE_RTU  # Mode to be used (RTU or ascii mode)

        # Good practice to clean up before and after each execution
        self.instrument.clear_buffers_before_each_transaction = True
        self.instrument.close_port_after_each_call = True

    def get_data_from_modbus(self):
        try:
            fetched_data = self.instrument.read_registers(self.register, 1, self.function_code)

            fetched_data_scaled = round((fetched_data[0] * self.scaling), 1)
            return fetched_data_scaled

        except Exception as e:
            print("Err: ", str(e))
            fetched_data_scaled = "N/A"
            return fetched_data_scaled


class Measurement():
    def __init__(self, description, unit, sensors, python_function, additional_info):
        self.description = description
        self.unit = unit
        self.sensors = sensors
        self.python_function = python_function
        self.additional_info = additional_info
        self.value = "N/A"

    def run_calculation_function(self):
        try:
            if self.python_function == "standard":
                self.value = str(modbus_functions.standard(self.sensors, self.additional_info)) + " " + self.unit
            elif (hasattr(modbus_functions, self.python_function)):
                calc_function = getattr(modbus_functions, self.python_function)
                self.value = str(calc_function(self.sensors, self.additional_info))
            else:
                self.value = "python function was invalid"

            return self.value
        except Exception as e:
            print("Err: ", e)


class Page():
 def __init__(self, title, measurements):
        self.title = title
        self.measurements = measurements


def get_sensor_data(device_full_data, port_name, sensor_unit): #alt. name: get_device_data
    for device in device_full_data["ports"]:
        print(device)
        if device["port"] == port_name:
            print("in port if")
            sensor_register = device["register"]
            sensor_function_code = device["function_code"]
            if "units" in device:
                for unit_pair in device["units"]:  # Hier kann vielleicht später das Array anders entpackt werden (mit *)
                    if unit_pair["unit"] == sensor_unit:
                        sensor_scaling = unit_pair["scaling"]
                        return_var = {"sensor_register": sensor_register, "sensor_scaling": sensor_scaling,
                                      "sensor_function_code": sensor_function_code}
                        return return_var
            else:
                return_var = {"sensor_register": sensor_register, "sensor_scaling": 1,
                              "sensor_function_code": sensor_function_code}
                return return_var

    return -1


def get_sensor_unit(sensor_name):
    sensor_file = open(DEVICES_CONFIG_PATH + 'sensors.json', encoding='utf-8')
    sensor_full_data = json.load(sensor_file)
    # print(sensor_full_data)
    for sensor in sensor_full_data:
        if sensor["type"] == sensor_name:
            sensor_unit = sensor["unit"]
            return sensor_unit

    sensor_file.close()
    return ""


def load_config():
    config_file = open(CONFIG_PATH + 'main_config_file.json', encoding='utf-8')
    config_full_data = json.load(config_file)
    config_file.close()

    global all_pages
    all_pages = []
    for page in config_full_data[0]["pages"]:
        title = page["title"]
        page_measurements = []
        for measurements in page["sources"]:
            page_sensors = []
            port_arr = measurements["port"]
            python_function = "standard"
            if "python_function" in measurements:
                python_function = measurements["python_function"]
            description = measurements["description"]
            additional_info = {}
            if "additional_info" in measurements:
                additional_info = measurements["additional_info"]

            unit = ""
            port_counter = 0
            for port in port_arr:
                device_id = list(port.keys())[port_counter] # example: QBM1
                port_id = port[device_id]  # example: AI1
                port_counter += 1

                for device in config_full_data[0]["devices"]:
                    if device["id"] == device_id:
                        # If the device has ports that can have different sensors attached (on a QBM for example),
                        # the sensor type has to be checked
                        if "sensors" in device:
                            for sensor_port in device["sensors"]:
                                if sensor_port["port"] == port_id:
                                    sensor_type = sensor_port["type"]
                                    unit = get_sensor_unit(sensor_type)
                        else:
                            unit = get_sensor_unit(port_id)

                        device_file = open(DEVICES_CONFIG_PATH + device["device"] + '.json', encoding='utf-8')
                        device_full_data = json.load(device_file)
                        device_file.close()

                        print(port_id, unit)

                        sensor_data = get_sensor_data(device_full_data, port_id, unit)

                        print("sensor_data: ", sensor_data)

                        scaling = sensor_data["sensor_scaling"]
                        register = sensor_data["sensor_register"]
                        function_code = sensor_data["sensor_function_code"]

                        page_sensors.append(Sensor(baud_rate=device["baud_rate"], mb_address=device["mbaddress"], parity=device["parity"], stop_bits=device["stop_bits"], register=register, scaling=scaling, function_code=function_code, zero_based=device["zero_based"]))

            page_measurements.append(Measurement(description=description, unit=unit, sensors=page_sensors, python_function=python_function,
                            additional_info=additional_info))

        counter = 0
        last_slice = 0
        # If a Category has more than 5 elements it has to be splitted into two or more pages
        for measurement in page_measurements:
            counter += 1
            if ((counter % 5) == 0) or (counter == len(page_measurements)):
                # print(title)
                all_pages.append(Page(title=title, measurements=page_measurements[last_slice:counter]))
                last_slice = counter

    return all_pages


def data_refresh(app):
    global stop_thread
    stop_thread = False
    while stop_thread == False:
        # This looks better, because all pages are already loaded; but it might be more costly
        page_counter = 0
        for page in all_pages:
            measurement_counter = 0
            for measurement in page.measurements:
                value = measurement.run_calculation_function()
                app.set_page_text_at(page_counter, measurement_counter, measurement.description, value)
                # app.set_page_title_at(current_page, all_pages[current_page].title)
                measurement_counter += 1
            page_counter += 1

        time.sleep(0.4)


def data_threading(app):
    # Funktion zum Starten des Datenaktualisierungs-Threads
    global t1
    t1 = Thread(target=data_refresh, kwargs={'app': app}, daemon=True)
    t1.start()


"""def stop_threading():
    global stop_thread
    stop_thread = True
    t1.join()"""
