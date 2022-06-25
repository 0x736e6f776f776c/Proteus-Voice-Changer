import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import wave as wv
import numpy as np
import sys
from aubio import source, pitch
import tkinter.font as tkf
import tkinter.messagebox as mb

# Amount of fractions the sound will be processed in
fr = 25
start = bool(True)
multi_missing_files = bool(None)
mimic_enabled = True
manual_enabled = False
wave_input, wave_modifier, wave_output, shifting, missing_file, output_file, pitch_set = "", "", "", "", "", "", False

# Defining the function to get the (average) pitch from the modifier
def get_pitch(filename, average_frequency):
    win_s = 4096
    hop_s = 512 

    s = source(filename, samplerate, hop_s)
    samplerate = s.samplerate

    tolerance = 0.8

    pitch_o = pitch("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(tolerance)

    pitches = []
    confidences = []

    total_frames = 0
    while True:
        samples, read = s()
        pitch = pitch_o(samples)[0]
        pitches += [pitch]
        confidence = pitch_o.get_confidence()
        confidences += [confidence]
        total_frames += read
        if read < hop_s: break

    average_frequency =  int(np.array(pitches).mean())
    return average_frequency

def file_error(preoutput):
    if preoutput == True:
        if manual_enabled == True:
            if pitch_set == False:
                error("Missing pitch", "It seems there is no set pitch.")
            elif ".wav" not in input_file.get() and ".wav" in output_file:
                error("Missing File", "It seems there is no input file.")
            elif ".wav" in input_file.get() and ".wav" not in output_file:
                error("Missing File", "It seems there is no output file.")
            elif ".wav" not in input_file.get() and ".wav" not in output_file:
                error("Missing Files", "It seems there is no input file and no output file.")
        else: # Mimic mode
            if ".wav" not in input_file.get() and ".wav" not in modifier_file.get() and ".wav" not in output_file:
                multi_missing_files = True
                error("Missing Files", "It seems there is no input file, no modifier file and no output file.")
            elif ".wav" not in input_file.get() and ".wav" not in modifier_file.get() and ".wav" in output_file:
                error("Missing Files", "It seems there is no input file and no modifier file.")
                multi_missing_files = True
            elif ".wav" not in input_file.get() and ".wav" in modifier_file.get() and ".wav" not in output_file:
                error("Missing Files", "It seems there is no input file and no output file.")
                multi_missing_files = True
            elif ".wav" in input_file.get() and ".wav" not in modifier_file.get() and ".wav" not in output_file:
                error("Missing Files", "It seems there is no modifier file and no output file.")
                multi_missing_files = True
            elif ".wav" not in input_file.get() and ".wav" in modifier_file.get() and ".wav" in output_file:
                multi_missing_files = False
                missing_file = "input"
            elif ".wav" in input_file.get() and ".wav" not in modifier_file.get() and ".wav" in output_file:
                multi_missing_files = False
                missing_file = "modifier"
            elif ".wav" in input_file.get() and ".wav" in modifier_file.get() and ".wav" not in output_file:
                multi_missing_files = False
                missing_file = "output"
            if multi_missing_files == False:
                error("Missing File", "It seems there is no {} file.".format(missing_file))
    else: # Pre-output select
        if manual_enabled == True:
            if pitch_set == False:
                error("Missing pitch", "It seems there is no set pitch.")
            else:
                error("Missing File", "It seems there is no input file.")
        else: # Mimic mode
            if ".wav" not in input_file.get() and ".wav" not in modifier_file.get():
                error("Missing Files", "It seems there is no input file and no modifier file.")
                multi_missing_files = True
            elif ".wav" not in input_file.get() and ".wav" in modifier_file.get():
                multi_missing_files = False
                missing_file = "input"
            elif ".wav" in input_file.get() and ".wav" not in modifier_file.get():
                multi_missing_files = False
                missing_file = "modifier"
            if multi_missing_files == False:
                error("Missing File", "It seems there is no {} file.".format(missing_file))

# Browse file method and store filename in the right variable / Set pitch method
def browseFiles(needed_file, label):
    global shifting
    global pitch_set
    if manual_enabled == True and label != input_file_label:
        try:
           int(input_set_pitch.get())
        except ValueError:
            error('Value Error', 'You can only enter whole numbers in this field.')
        finally:
            if input_set_pitch.get() == '':
                input_set_pitch.set('0')
            shifting = int(input_set_pitch.get())
            set_pitch_entry.delete(0, 2)
            hertz_label.config(text = '{} Hz'.format(str(shifting)))
            pitch_set = True
    if mimic_enabled == True or label == input_file_label:
        filename = filedialog.askopenfilename(initialdir = "/",
                                              title = "Select a file",
                                              filetypes = [("Wave files (.wav)", "*.wav")])
        needed_file.set(" ")
        needed_file.set(filename)
        if ".wav" in filename:
            label.config(textvariable = needed_file)
            center(window)
        else:
            label.config(textvariable = arrows)
            center(window)

# Tkinter messagebox functions
def error(title, message):
    mb.showwarning(title = title, message = message)
def info(title, message):
    mb.showinfo(title = title, message = message)

def help():
    if mimic_enabled == True:
        info("Instructions", "You are currently in mimic mode. On the left side, select the file that you want to adjust the pitch/voice of. On the right side, select the file from which you want to use the pitch/voice. Thanks for using Proteus Voice Changer :]")
    elif manual_enabled == True:
        info("Instructions", "You are currently in manual mode. On the left side, select the file that you want to adjust the pitch/voice of. On the right side, choose the pitch in Hertz that you want to change your input audio's pitch to. Thanks for using Proteus Voice Changer :]")

# Function for the modification button, modification of the input file
def modify():
    if ".wav" in input_file.get() and ".wav" in modifier_file.get() and ".wav" in output_file or manual_enabled == True and ".wav" in input_file.get() and pitch_set == True:
        # Prompting save as file window for the output file
        output_file = " "
        output_file = filedialog.asksaveasfilename(initialdir = "/",
                                               title = "Save your output file",
                                               filetypes = [("Wave files (.wav)","*.wav")])
        if ".wav" in output_file:
            # Declaring global variables
            global wave_input
            global wave_modifier
            global wave_output
            if ".wav" in output_file:
                # Opening the input and output files
                wave_input = wv.open(input_file.get(), 'rb')
                wave_output = wv.open(output_file, 'wb')
                # Setting the parameters from the input file
                input_params = list(wave_input.getparams())
                # Setting the parameter for number of samples to zero
                input_params[3] = 0
                # Making a tupple for the parameters
                input_params = tuple(input_params)
                # Setting output parameters to the input parameters
                wave_output.setparams(input_params)
                # Setting frame processing with fr to try to avoid reverb as much as possible
                processing = wave_input.getframerate() // fr
                # Count of the entire file
                count = int(wave_input.getnframes() / processing)
                # Setting the shift
                if mimic_enabled == True:
                    get_pitch(modifier_file.get(), shifting)
                elif manual_enabled == True:
                    shift = int(shifting) // fr
                # Checking for amount of channels (1 = mono, 2 = stereo)
                channels = wave_input.getnchannels()
                for num in range(count):
                    try:
                        data = np.frombuffer(wave_input.readframes(processing), dtype = np.int16) # Reading the data 
                        if channels == 2:
                            left, right = data[0::2], data[1::2] # Splitting the data into a left and a right channel
                            lf, rf = np.fft.rfft(left), np.fft.rfft(right) # Extracting the framerate from the data
                            lf, rf = np.roll(left, shift), np.roll(right, shift) # Rolling the array to change the pitch
                            lf[0:shift], rf[0:shift] = 0, 0 # Fixes highest frequencies rolling over to the lower ones
                            nl, nr = np.fft.irfft(lf), np.fft.irfft(rf) # Converting the signal back to amplitude
                            ns = np.column_stack((nl, nr)).ravel().astype(np.int16) # Putting the two channels back together
                            wave_output.writeframes(ns.tobytes()) # Writing the data to the output file
                        elif channels == 1:
                            dataf = np.fft.rfft(data) # Extracting the framerate from the data
                            dataf = np.roll(dataf, shift) # Rolling the array to change the pitch
                            dataf[0:shift] = 0 # Fixes highest frequencies rolling over to the lower ones
                            ndata = np.fft.irfft(dataf) # Converting the signal back to amplitude
                            wave_output.writeframes(ndata.tobytes()) # Writing the data to the output file
                    except e:
                        error("Error", e)
                wave_input.close()
                wave_output.close()
                info("Completed", "Output succesfully saved in {}. Thanks for using Proteus Voicechanger.".format(output_file))
                output_file = " "
        else:
            file_error(False)
    else:
        file_error(True)

def manual_mode(top_label, middle_label, button):
    top_label.config(text = 'Pitch')
    button.config(text = 'Set pitch')
    set_pitch_entry.grid(column = 2, row = 1, padx = (3, 3))
    modifier_file.set(" ")
    hertz_label.grid(column = 2, row = 2)

def mimic_mode(top_label, middle_label, button):
    top_label.config(text = 'Modifier file')
    button.config(text = 'Browse files')
    middle_label.config(textvariable = arrows)
    set_pitch_entry.grid_forget()
    hertz_label.grid_forget()
    hertz_label.config(text = 'Hz')

def frame_state_machine(button):
    global manual_enabled
    global mimic_enabled
    if frame_button_text.get() == "Mimic mode" and mimic_enabled == False:
        if manual_enabled == True:
            manual_enabled = False
        frame_button_text.set("Manual mode")
        mimic_mode(modifier_label, modifier_file_label, modifier_button)
        mimic_enabled = True

    elif frame_button_text.get() == "Manual mode" and manual_enabled == False:
        if mimic_enabled == True:
            mimic_enabled = False
        frame_button_text.set("Mimic mode")
        manual_mode(modifier_label, modifier_file_label, modifier_button)
        manual_enabled = True

# Function to center the window in the beginning
def center(window):
    window.update_idletasks()
    width = window.winfo_width()
    frm_width = window.winfo_rootx() - window.winfo_x()
    window_width = width + 2 * frm_width
    height = window.winfo_height()
    titlebar_height = window.winfo_rooty() - window.winfo_y()
    window_height = height + titlebar_height + frm_width
    x = window.winfo_screenwidth() // 2 - window_width // 2
    y = window.winfo_screenheight() // 2 - window_height // 2
    window.geometry("+{}+{}".format(x, y))
    window.deiconify()
                                          
# Root window configuration
window = tk.Tk()
window.resizable(height = None, width = None)
window.title("Proteus Voice Changer")
window.config(background = "#00e5e5")

style = ttk.Style()
style.configure("TFrame", background = "#00e5e5")
style.configure("Labeltxt.TLabel", background = "#00e5e5")
style.configure("TFrame", background = "#00e5e5", relief = "flat")
style.configure("Outputbutton.TButton", padding = 30)

mainframe = ttk.Frame(window)
mainframe.grid(column = 0, row = 0)
mainframe.rowconfigure(0, weight = 1)
mainframe.rowconfigure(1, weight = 1)
mainframe.rowconfigure(2, weight = 1)
mainframe.rowconfigure(3, weight = 1)
mainframe.rowconfigure(4, weight = 1)
mainframe.rowconfigure(5, weight = 1)
mainframe.columnconfigure(0, weight = 1)
mainframe.columnconfigure(1, weight = 1)
mainframe.columnconfigure(2, weight = 1)
width = mainframe.winfo_width()
height = mainframe.winfo_height()

input_file = tk.StringVar()
modifier_file = tk.StringVar()
frame_button_text = tk.StringVar()
hertz = tk.StringVar()
arrows = tk.StringVar()
input_set_pitch = tk.StringVar()

arrows.set("⇊")
hertz.set("Hz")
input_file.set(" ")
modifier_file.set(" ")

# Trident icon declaration
window.iconbitmap("/Media/trident.ico")

# Proteus image
proteus_image = tk.PhotoImage(file = "/Media/proteus.gif")

# Help question mark image
help_image = tk.PhotoImage(file = "/Media/help.gif")

# Fonts
txt_font = tkf.Font(family = "Segoe UI Semibold", size=12)
file_font = tkf.Font(family = "Georgia Pro Black", size = 12)
entry_font = tkf.Font(family = "Georgia Pro Cond Light", size = 10)

# Initiating the labels
#top_label = ttk.Label(mainframe,
                  #text = "Welcome. On the left side, select the file that you want to adjust the pitch/voice of. On the left side, select the file from which you want to use the pitch/voice. Thanks for using Proteus :)",
                  #width = "0"
                  #)

input_label = ttk.Label(mainframe,
                        text = "Input file",
                        width = "0",
                        style = "Labeltxt.TLabel",
                        font = txt_font
                        )

output_label = ttk.Label(mainframe,
                         text = "Output file",
                         width = "0",
                         style = "Labeltxt.TLabel",
                         font = txt_font
                         )
                    
modifier_label = ttk.Label(mainframe,
                           text = "Modifier file",
                           width = "0",
                           style = "Labeltxt.TLabel",
                           font = txt_font
                           )   

input_file_label = ttk.Label(mainframe,
                             textvariable = input_file,
                             width = "0",
                             style = "Labeltxt.TLabel",
                             font = file_font 
                             )

modifier_file_label = ttk.Label(mainframe,
                                textvariable = modifier_file,
                                width = "0",
                                style = "Labeltxt.TLabel",
                                font = file_font
                                )

hertz_label = ttk.Label(mainframe,
                        text = "Hz",
                        style = "Labeltxt.TLabel",
                        font = entry_font
                        )

#Initiating buttons
input_button = ttk.Button(mainframe,
                          text = "Browse files",
                          command = lambda : browseFiles(input_file, input_file_label))

modifier_button = ttk.Button(mainframe,
                           text = "Browse files",
                           command = lambda : browseFiles(modifier_file, modifier_file_label))

modification_button_image = tk.Button(mainframe,
                              image = proteus_image,
                              command = lambda : modify(),
                              fg = "#00e5e5",
                              bg = "#00e5e5")

frame_button = ttk.Button(mainframe,
                          textvariable = frame_button_text,
                          command = lambda : frame_state_machine(frame_button))

help_button = ttk.Button(mainframe,
                         image = help_image,
                         command = lambda : help(),
                         width = 5)

# Initiating entries
set_pitch_entry = tk.Entry(master = mainframe,
                           textvariable = input_set_pitch,
                           font = entry_font,
                           width = 6)

# Geometry for the labels
input_label.grid(column = 0, row = 0)
output_label.grid(column = 1, row = 0)
modifier_label.grid(column = 2, row = 0)
input_file_label.grid(column = 0, row = 2, padx=(50, 50))
modifier_file_label.grid(column = 2, row = 2, padx=(50, 50))
hertz_label.grid(column = 2, row = 3)

# Geometry for the buttons
input_button.grid(column = 0, row = 3)
modifier_button.grid(column = 2, row = 3)
frame_button.grid(column = 1, row = 3)
modification_button_image.grid(column = 1, row = 2, pady = (20, 20))
help_button.grid(column = 1, row = 3, padx = (188, 0), pady= (0, 14))

# Necessary start declarations and functions
if start == True:
    center(window)
    manual_enabled = False
    mimic_enabled = True
    start = False
    file_progressing = ''
    input_file_label.config(textvariable = arrows)
    modifier_file_label.config(textvariable = arrows)
    hertz_label.grid_forget()

if mimic_enabled == True:
    frame_button_text.set("Manual mode")

# Debugging
# screen_width = window.winfo_width()
# screen_height = window.winfo_height()
# print(str(screen_height) + "x" + str(screen_width))

window.mainloop()
