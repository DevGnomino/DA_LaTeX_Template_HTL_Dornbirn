import customtkinter as ctk
from PIL import Image
import tkinter
from tkinter import Canvas
import modbus
import globals_
import usb_detection
import RPi.GPIO as GPIO
import time
import os

if os.environ.get('DISPLAY','') == '': # Uses screen if it doesnt find a screen
   os.environ.__setitem__('DISPLAY', ':0.0')

# Initial Setup
ctk.set_default_color_theme("blue")  # Supported themes: green, dark-blue, blue
app_width, app_height = 800, 480
light_mode = True  # True for Light Mode and False for Dark Mode

if light_mode:
    ctk.set_appearance_mode("Light")
    text_color = "#EBEBEB"
    title_color = "#11345D"
    frame_color = "#496077"

    # frame_color = "#496077"  # blueish grey
    # frame_color = "#304D6D" #blue
    # frame_color = "#283233" #bösch dark grey
else:
    ctk.set_appearance_mode("Dark")
    text_color = "#242424"
    frame_color = "#EBEBEB"


# global globals.current_page
# globals.current_page = 0

class TitleFrame(ctk.CTkFrame):
    def __init__(self, master, title, **kwargs):
        super().__init__(master, width=800, height=60, fg_color=text_color, **kwargs)

        title_font = ctk.CTkFont(family="Roboto", size=32)

        self.title_lbl = ctk.CTkLabel(master=self, text=title, width=700, height=45, fg_color="transparent",
                                      text_color=title_color, anchor=ctk.CENTER, font=title_font)
        self.title_lbl.place(relx=0.5, rely=0.12, anchor=ctk.N)

    def set_title(self, title):
        self.title_lbl.configure(text="title")


class MeasurementFrame(ctk.CTkFrame):
    def __init__(self, master, measurement, value, **kwargs):
        super().__init__(master, width=770, height=55, fg_color=title_color, **kwargs)

        text_font = ctk.CTkFont(family="Roboto", size=33)

        self.measurement_lbl = ctk.CTkLabel(master=self, text=measurement,
                                            width=485, height=52,
                                            fg_color="transparent", text_color=text_color,
                                            anchor=ctk.W, font=text_font)
        self.measurement_lbl.place(relx=0.34, rely=0.5, anchor=ctk.CENTER)

        self.value_lbl = ctk.CTkLabel(master=self, text=value,
                                      width=190, height=52,
                                      fg_color="transparent", text_color=text_color,
                                      anchor=ctk.CENTER, font=text_font)
        self.value_lbl.place(relx=0.84, rely=0.5, anchor=ctk.CENTER)

        canvas = Canvas(master=self, width=2, height=50,
                        bg=text_color, highlightthickness=0)
        canvas.place(relx=0.67, rely=0.5, anchor=ctk.CENTER)

    def set_text(self, measurement, value):
        self.measurement_lbl.configure(text=measurement)
        self.value_lbl.configure(text=value)


class PageFrame(ctk.CTkFrame):
    def __init__(self, master, title, parameters, **kwargs):
        super().__init__(master, 800, 515, fg_color="transparent", **kwargs)
        self.measurement_frames = []
        self.title_frame = TitleFrame(
            master=master, title=title, corner_radius=0)

        for parameter in parameters:
            frame = MeasurementFrame(
                master=master, measurement=parameter.description, value="N/A", corner_radius=15)
            self.measurement_frames.append(frame)

    def show_frame(self, show_or_hide):
        if show_or_hide:
            self.title_frame.place(relx=0.5, rely=0.0, anchor=ctk.N)
            self.title_frame.tkraise()
        else:
            self.title_frame.place_forget()

        spacing = 0.0
        for my_frame in self.measurement_frames:
            if show_or_hide:
                my_frame.place(relx=0.5, rely=(
                        0.20 + spacing), anchor=ctk.CENTER)
                my_frame.tkraise()
            else:
                my_frame.place_forget()
            spacing += 0.143  # 0.1335

    def set_title_at(self, title):
        self.title_frame.set_title(title)

    def set_text_at(self, index, measurement, value):
        # ZUM TESTEN, so werden Fehler abgefangen; wird aber eigentlich nicht benötigt!
        if index >= 0 and index < len(self.measurement_frames):
            self.measurement_frames[index].set_text(measurement, value)


class App(ctk.CTk):
    def __init__(self, all_pages, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Bösch RLT Anzeige")
        self.geometry(f"{app_width}x{app_height}")
        self.attributes('-fullscreen', True)
        self.resizable(False, False)
        self.config(cursor="none")

        boesch_logo = ctk.CTkImage(light_image=Image.open("/home/pi/Documents/00_boesch_logo_transparent.png"),
                                   dark_image=Image.open(
                                       "/home/pi/Documents/00_boesch_logo_transparent_dark.png"),
                                   size=(230, 230 * (1 / 3)))

        self.img_label = ctk.CTkLabel(master=self, image=boesch_logo, text="")
        self.img_label.place(relx=0.5, rely=0.915, anchor=ctk.CENTER)

        global page_frame_list
        page_frame_list = []
        global page_indicator_list
        page_indicator_list = []

        for page in all_pages:  # Creates Frames based on the sensor data
            page_frame_list.append(PageFrame(master=self, title=page.title,
                                             parameters=page.measurements))

        print(len(page_frame_list))
        page_frame_list[globals_.current_page].show_frame(True)

        # Diese Buttons werden später mit Physischen Tastern ersetzt!!!
        """self.last_page_button = ctk.CTkButton(
            master=self, text="Last Page", width=50, command=last_page, fg_color=frame_color)
        self.last_page_button.place(relx=0.065, rely=0.93, anchor=ctk.CENTER)

        self.next_page_button = ctk.CTkButton(
            master=self, text="Next Page", width=50, command=next_page, fg_color=frame_color)
        self.next_page_button.place(relx=0.17, rely=0.93, anchor=ctk.CENTER)"""

        # add page indicator responsiveness
        start_x_position = 0.975 - len(page_frame_list) / 45.0

        if len(page_frame_list) > 1:
            for i in range(0, len(page_frame_list)):
                page_indicator_list.append(ctk.CTkButton(master=self, width=15, height=15, text="", corner_radius=50,
                                                         fg_color=(
                                                             "#898989" if i == globals_.current_page else "#D9D9D9")))
                page_indicator_list[i].place(
                    relx=start_x_position + i / 45.0, rely=0.93, anchor=ctk.CENTER)

    def set_page_title_at(self, page_index, title):
        page_frame_list[page_index].set_title_at(title)

    def set_page_text_at(self, page_index, measurement_index, measurement, value):
        # Wieder zum Fehler abfangen, eigentlich nicht nötig
        if page_index >= 0 and page_index < len(page_frame_list):
            page_frame_list[page_index].set_text_at(
                measurement_index, measurement, value)


def last_page(channel):
    if len(page_frame_list) < 2:
        return

    globals_.current_page -= 1
    if globals_.current_page < 0:
        globals_.current_page = len(page_frame_list) - 1

    for i in range(0, len(page_frame_list)):
        page_indicator_list[i].configure(fg_color="#D9D9D9")
    page_indicator_list[globals_.current_page].configure(fg_color="#898989")

    for f in page_frame_list:
        f.show_frame(False)
    page_frame_list[globals_.current_page].show_frame(True)
    print("last page loaded")


def next_page(channel):
    if len(page_frame_list) < 2:
        return

    globals_.current_page += 1
    if globals_.current_page >= len(page_frame_list):
        globals_.current_page = 0

    for i in range(0, len(page_frame_list)):
        page_indicator_list[i].configure(fg_color="#D9D9D9")
    page_indicator_list[globals_.current_page].configure(fg_color="#898989")

    for f in page_frame_list:
        f.show_frame(False)
    page_frame_list[globals_.current_page].show_frame(True)
    print("Next page loaded")

def last_page_button_clicked(channel):
    last_page(channel)
    close_app(channel)

def setup_buttons():
    last_page_button = 37
    next_page_button = 38

    #GPIO.BOARD refers to physical pin numbers
    #GPIO.BCM refers to GPIO pin numbers

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(last_page_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(last_page_button, GPIO.FALLING, callback=last_page_button_clicked, bouncetime=300)

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(next_page_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(next_page_button, GPIO.FALLING, callback=next_page, bouncetime=300)
    #GPIO.add_event_detect(last_page_button, GPIO.FALLING, callback=close_app, bouncetime=300)


def close_app(channel):
    # for testing purposes, to close the program on long button press
    start_time = time.time()
    while GPIO.input(channel) == GPIO.LOW:
        #time.sleep(0.1)
        elapsed_time = time.time() - start_time
        if elapsed_time >= 5:
            print("Button pressed for more than 5 seconds. Exiting.")
            GPIO.cleanup()
            app.quit()

if __name__ == "__main__":
    copy_error = usb_detection.usb_routine()
    if copy_error:
        exit
    all_pages = modbus.load_config()
    global app
    app = App(all_pages)
    setup_buttons()
    modbus.data_threading(app)
    # Runs the app
    app.mainloop()
