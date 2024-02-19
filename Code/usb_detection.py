import os
import time
import tkinter as tk
import customtkinter as ctk 

if os.environ.get('DISPLAY','') == '':
    os.environ.__setitem__('DISPLAY', ':0.0')

def start_window(message):
    msg_window = tk.Tk()  # create the Tk window like you normally do
    msg_window.title("Meldung")
    msg_window.attributes('-fullscreen', True)

    ctk.set_appearance_mode("Light") # Other: "Light", "System" (only macOS)
    msg_window.configure(background="white")
    label = ctk.CTkLabel(master=msg_window,
                        text_color="red",
                        font = ('Roboto', 26),
                        text=message,
                        wraplength=450)
    label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    msg_window.after(7000, lambda: msg_window.destroy())
    msg_window.mainloop()

def check_if_files_exists(config_path, device_config_path):
    if not os.path.exists(config_path):
        start_window("RLT_Config Ordner existiert nicht")
        return False
    if not os.path.isfile(config_path + "main_config_file.json"):
        start_window("main_config_file.json existiert nicht")
        return False
    if not os.path.exists(device_config_path):
        start_window("devices Ordner existiert nicht")
        return False
    if not os.path.exists(device_config_path + "sensors.json"):
        start_window("devices/sensors.json existiert nicht")
        return False
    return True

def copy_from_usb():
    usb_config_path = "/home/pi/Documents/Config/RLT_Config/"
    usb_device_config_path = "/home/pi/Documents/Config/RLT_Config/devices/"
    config_path = "/home/pi/Documents/RLT_Config/"
    device_config_path = "/home/pi/Documents/RLT_Config/devices/"

    port = ""
    time.sleep(5)
    while True:
        if (os.system("mount | grep sda1") != 256):
            port = "sda1"
            break
        elif (os.system("mount | grep sdb1") != 256):
            port = "sdb1"
            break
        elif (os.system("mount | grep sdc1") != 256):
            port = "sdc1"
            break
        elif (os.system("mount | grep sdd1") != 256):
            port = "sdd1"
            break

        if (check_if_files_exists(config_path, device_config_path)):
            return 1
            
    #is_mounted = os.system("mount | grep " +  port)
    #if (is_mounted != 256): # Runtime error --> no drive mounted
        
    start_window("USB-Stick wurde gemountet: " + port)

    os.system("sudo umount /dev/" + port)
    os.system("sudo mount /dev/" + port + " /home/pi/Documents/Config")
    #is_mounted = os.system("mount | grep sda1")
    #print(is_mounted)
    error_free = check_if_files_exists(usb_config_path, usb_device_config_path)  
    
    if error_free:
        os.system("cp -r ~/Documents/Config/RLT_Config ~/Documents/")
    else:
        os.system("sudo umount /dev/" + port)
        return -1

    os.system("sudo umount /dev/" + port)
    #os.system("sudo eject /dev/" + port) 
    #os.system("udisk --detach /dev/" + port)
    return 0

def usb_routine():
    copy_status = copy_from_usb()
    if copy_status == -1:
        return True
    elif copy_status == 0:
        start_window("Config Dateien wurden kopiert. Entferne nun den USB")   
    elif copy_status == 1: 
        start_window("Kein USB-Stick gefunden und Config bereits vorhanden")
    return False
