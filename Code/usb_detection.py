import os
import time
import tkinter as tk
import customtkinter as ctk 

if os.environ.get('DISPLAY','') == '':
    os.environ.__setitem__('DISPLAY', ':0.0')

def start_window(error_message):
    root_tk = tk.Tk()  # create the Tk window like you normally do
    root_tk.geometry("500x250+100+90")
    root_tk.title("Meldung")
    root_tk.attributes('-fullscreen', True)

    ctk.set_appearance_mode("Light") # Other: "Light", "System" (only macOS)
    root_tk.configure(background="white")
    label = ctk.CTkLabel(master=root_tk,
                        text_color="red",
                        font = ('Roboto', 26),
                        text=error_message,
                        wraplength=450)
    label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    root_tk.after(7000, lambda: root_tk.destroy())
    root_tk.mainloop()

def check_if_files_exists(config_path, device_config_path, verbose):    
    path_exists = os.path.exists(config_path)
    if not path_exists:
        if (verbose):
            start_window("RLT_Config Ordner existiert nicht")
        return False
    path_exists = os.path.isfile(config_path + "main_config_file.json")
    if not path_exists:
        if (verbose):
            start_window("main_config_file.json existiert nicht")
        return False
    path_exists = os.path.exists(device_config_path)
    if not path_exists:
        if (verbose):
            start_window("Device Ordner existiert nicht")
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

        if (check_if_files_exists(config_path, device_config_path, False)):
            return 1

        time.sleep(5)
    #is_mounted = os.system("mount | grep " +  port)
    #if (is_mounted != 256): # Runtime error --> no drive mounted
        
    start_window("USB-Stick wurde gemountet: " + port)

    os.system("sudo umount /dev/" + port)
    os.system("sudo mount /dev/" + port + " /home/pi/Documents/Config")
    #is_mounted = os.system("mount | grep sda1")
    #print(is_mounted)
    error_free = check_if_files_exists(usb_config_path, usb_device_config_path, True)  
    
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
    copy_error = copy_from_usb()
    if copy_error == -1:
        return True
    elif copy_error == 0:
        start_window("Config Dateien wurden kopiert. Entferne nun den USB")   
    elif copy_error == 1: 
        start_window("Kein USB-Stick gefunden und Config bereits vorhanden")
    return False
