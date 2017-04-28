import tkinter as tk
import tkinter.messagebox
import serial
import threading
import _thread
import sys
import glob
import time

errors = {'20': 'Over-Speed Error', '30': 'Overflow Error', '52': 'Communication Command Error',
          '90': 'Tolerance Setup Error', '95P': 'Preset Value Error', '95G': 'Upper Limit Error',
          '95D': 'Lower Limit Error'}


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        temp_list = glob.glob('/dev/tty[A-Za-z]*')

        result = []
        for a_port in temp_list:

            try:
                s = serial.Serial(a_port)
                s.close()
                result.append(a_port)
            except serial.SerialException:
                pass

        return result
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def port_baud_id_select(ports):
    master = tk.Tk()

    master['padx'] = 40
    master['pady'] = 40

    port_frame = tk.Frame(master, width=200)
    baud_frame = tk.Frame(master, width=200)
    id_frame = tk.Frame(master, width=200)

    port_label = tk.Label(port_frame)
    port_label["text"] = "Choose Port"
    port_label.pack(side=tk.LEFT)

    baud_label = tk.Label(baud_frame)
    baud_label["text"] = "Choose Baud rate"
    baud_label.pack(side=tk.LEFT)

    id_label = tk.Label(id_frame)
    id_label["text"] = "Enter ID No."
    id_label.pack(side=tk.LEFT)

    port = tk.StringVar(port_frame)
    baud = tk.StringVar(baud_frame)
    id_number = tk.StringVar(id_frame)

    # idlabel = tk.Label(master, text="ID Number")

    port.set(ports[0])  # default value
    baud.set("9600")
    id_number.set('00')

    port_choice = tk.OptionMenu(port_frame, port, *ports)
    baud_choice = tk.OptionMenu(baud_frame, baud, "4800", "9600")
    id_no = tk.Entry(id_frame, textvariable=id_number)

    port_frame.pack()
    baud_frame.pack()
    id_frame.pack()

    port_choice.pack()
    baud_choice.pack()
    id_no.pack()
    # idlabel.pack()

    def ok():
        print("port is", port.get())
        print("baud is", baud.get())
        print("ID is", id_number.get())

        master.destroy()

    button = tk.Button(master, text="OK", command=ok)
    button.pack()

    tk.mainloop()
    return [port.get(), int(baud.get()), id_number.get()]

port_baud = port_baud_id_select(serial_ports())

ser = serial.Serial(port_baud[0], port_baud[1], stopbits=2)

# Commands ####
set_zero_command = bytes(('CR' + port_baud[2] + '\r\n').encode("ascii"))
set_system_preset_command = bytes(('DS' + port_baud[2] + ',PC\r\n').encode("ascii"))
set_preset_value_command = bytes(('CP' + port_baud[2] + '\r\n').encode("ascii"))
read_preset_value_command = bytes(('DP' + port_baud[2] + ',OUT\r\n').encode("ascii"))
set_mode_normal_command = bytes(('CN' + port_baud[2] + '\r\n').encode("ascii"))
set_mode_max_command = bytes(('CX' + port_baud[2] + '\r\n').encode("ascii"))
set_mode_min_command = bytes(('CM' + port_baud[2] + '\r\n').encode("ascii"))
set_mode_TIR_command = bytes(('CW' + port_baud[2] + '\r\n').encode("ascii"))
read_data_command = bytes(('GA' + port_baud[2] + '\r\n').encode("ascii"))
cancel_peak_hold_command = bytes(('CL' + port_baud[2] + '\r\n').encode("ascii"))
set_peak_zero_command = bytes(('DS' + port_baud[2] + ',XM-ZERO\r\n').encode("ascii"))
tolerance_judgment_on_command = bytes(('DJ' + port_baud[2] + ',ON\r\n').encode("ascii"))
tolerance_judgment_off_command = bytes(('DJ' + port_baud[2] + ',OFF\r\n').encode("ascii"))
set_upper_limit_command = bytes(('CG' + port_baud[2] + '\r\n').encode("ascii"))
set_lower_limit_command = bytes(('CD' + port_baud[2] + '\r\n').encode("ascii"))
read_upper_limit_command = bytes(('DJ' + port_baud[2] + ',GOUT\r\n').encode("ascii"))
read_lower_limit_command = bytes(('DJ' + port_baud[2] + ',DOUT\r\n').encode("ascii"))
read_judgment_command = bytes(('DJ' + port_baud[2] + ',OUT\r\n').encode("ascii"))
center_analog_display_command = bytes(('DA' + port_baud[2] + '\r\n').encode("ascii"))
enable_function_lock_command = bytes(('DF' + port_baud[2] + ',LOCK\r\n').encode("ascii"))
disable_function_lock_command = bytes(('DF' + port_baud[2] + ',FREE\r\n').encode("ascii"))
read_function_lock_status_command = bytes(('DF' + port_baud[2] + ',OUT\r\n').encode("ascii"))
set_units_mm_command = bytes(('DU' + port_baud[2] + ',MM\r\n').encode("ascii"))
set_units_inch_command = bytes(('DU' + port_baud[2] + ',IN\r\n').encode("ascii"))
read_units_command = bytes(('DU' + port_baud[2] + ',OUT\r\n').encode("ascii"))
set_res_0005_mm_command = bytes(('DR' + port_baud[2] + ',D0.000500\r\n').encode("ascii"))
set_res_001_mm_command = bytes(('DR' + port_baud[2] + ',D0.001000\r\n').encode("ascii"))
set_res_00002_in_command = bytes(('DR' + port_baud[2] + ',D0.000020\r\n').encode("ascii"))
set_res_00005_in_command = bytes(('DR' + port_baud[2] + ',D0.000050\r\n').encode("ascii"))
set_res_0001_in_command = bytes(('DR' + port_baud[2] + ',D0.000100\r\n').encode("ascii"))
read_resolution_command = bytes(('DR' + port_baud[2] + ',DOUT\r\n').encode("ascii"))
# set_analog_range_command = bytes(('DR' + port_baud[2] + '\r\n').encode("ascii"))
read_analog_range_command = bytes(('DR' + port_baud[2] + ',AOUT\r\n').encode("ascii"))
set_count_direction_positive_command = bytes(('DD' + port_baud[2] + ',NORM\r\n').encode("ascii"))
set_count_direction_negative_command = bytes(('DD' + port_baud[2] + ',REV\r\n').encode("ascii"))
read_count_direction_command = bytes(('DD' + port_baud[2] + ',OUT\r\n').encode("ascii"))
set_start_system_inc_command = bytes(('DS' + port_baud[2] + ',SIN\r\n').encode("ascii"))
set_start_system_use_last_command = bytes(('DS' + port_baud[2] + ',SFREE\r\n').encode("ascii"))
read_start_system_command = bytes(('DS' + port_baud[2] + ',OUT\r\n').encode("ascii"))
reset_to_default_command = bytes(('DE' + port_baud[2] + ',RESET\r\n').encode("ascii"))


class Menu:

    def __init__(self):

        self.lock = threading.Lock()

        self.main_window = tk.Tk()
        self.main_window.title("ID-H Parameter Setting and Acquisition")
        self.main_window.geometry("1200x600")

        #  Frames
        self.reading_frame = tk.Frame(self.main_window, bg='Orange')  # Receiving DATAs
        self.parameter_frame = tk.Frame(self.main_window, bg='White')

        split = 0.5

        #  ReceiveLabel
        # self.ReceiveLabel = tk.Label(self.reading_frame, text='Received DATAs', bg='White', height=2, width=20)

        #  Data
        self.current_reading_label = tk.Label(self.reading_frame, bg="Blue", text='Current Reading :', font=("Helvetica", 24))
        self.data_value = tk.StringVar()

        self.data_value_label = tk.Label(self.reading_frame, bg='Green', textvariable=self.data_value,
                                         font=("Helvetica", 60))

        # PACKING!!! F2
        self.reading_frame.pack()
        self.reading_frame.place(relx=0, relwidth=split, relheight=split)
        self.parameter_frame.pack()
        self.parameter_frame.place(relx=split, relwidth=1.0 - split, relheight=1)

        # ReceiveLabel
        # self.ReceiveLabel.pack()
        # self.ReceiveLabel.place(x=100, y=10)
        # Reading
        self.current_reading_label.pack()
        # self.current_reading_label.place(x=50, y=80, height=20, width=150)
        self.data_value_label.pack()
        # self.data_value_label.place(x=250, y=80, height=75, width=600)
        self.data_value_label.place(y=80, x=50, height=100, width=500)

    # Buttons #####

        # quit ###
        self.quitButton = tk.Button(self.main_window, text='Quit', command=self.main_window.destroy, height=2, width=6)
        self.quitButton.pack()
        self.quitButton.place(x=50, y=500)

        # Set Zero ###

        self.setZeroButton = tk.Button(self.main_window, text='Set Zero', command=self.set_zero, height=2, width=6)
        self.setZeroButton.pack()
        self.setZeroButton.place(x=600, y=500)

    # Parameters #####

        # Tolerance Judgment ########
        self.tolerance_judgment_frame = tk.Frame(self.parameter_frame)

        # Tolerance On/Off
        self.tolerance_ONOFF_frame = tk.Frame(self.tolerance_judgment_frame, width=500)
        self.current_tolonoff = tk.StringVar(self.tolerance_ONOFF_frame)
        self.current_tolonoff.set(self.get_tolonoff())
        self.new_tolonoff = tk.StringVar(self.tolerance_ONOFF_frame)
        self.new_tolonoff.set(self.current_tolonoff.get())
        self.toleranceONOFF = tk.OptionMenu(self.tolerance_ONOFF_frame, self.new_tolonoff, "ON", "OFF")
        tolonoff_label = tk.Label(self.tolerance_ONOFF_frame)
        tolonoff_label["text"] = "Tolerance Judgment"
        tolonoff_label.pack(side=tk.LEFT)
        self.toleranceONOFF.pack(side=tk.RIGHT)
        self.tolerance_ONOFF_frame.pack()
        self.new_tolonoff.set("OFF")

        # Upper Tolerance Limit
        self.upper_limit_frame = tk.Frame(self.tolerance_judgment_frame)
        self.current_upper_limit = tk.StringVar(self.upper_limit_frame)
        self.current_upper_limit.set(self.read_upper_limit())
        self.new_upper_limit = tk.StringVar(self.upper_limit_frame)
        self.new_upper_limit.set(self.current_upper_limit.get())
        self.upper_limit_entry = tk.Entry(self.upper_limit_frame, textvariable=self.new_upper_limit)
        upper_limit_label = tk.Label(self.upper_limit_frame)
        upper_limit_label["text"] = "Upper Tolerance Limit"
        upper_limit_label.pack(side=tk.LEFT)
        self.upper_limit_frame.pack()
        self.upper_limit_entry.pack()

        # Lower Tolerance Limit
        self.lower_limit_frame = tk.Frame(self.tolerance_judgment_frame)
        self.current_lower_limit = tk.StringVar(self.lower_limit_frame)
        self.current_lower_limit.set(self.read_lower_limit())
        self.new_lower_limit = tk.StringVar(self.lower_limit_frame)
        self.new_lower_limit.set(self.current_lower_limit.get())
        self.lower_limit_entry = tk.Entry(self.lower_limit_frame, textvariable=self.new_lower_limit)
        lower_limit_label = tk.Label(self.lower_limit_frame)
        lower_limit_label["text"] = "Lower Tolerance Limit"
        lower_limit_label.pack(side=tk.LEFT)
        self.lower_limit_frame.pack()
        self.lower_limit_entry.pack()

        self.send_all_tol_button = tk.Button(self.tolerance_judgment_frame, text='Send All Tolerance Parameters',
                                             command=lambda: self.send_tol(self.new_tolonoff.get(), self.new_upper_limit.get(),
                                                                           self.new_lower_limit.get()))
        self.send_all_tol_button.pack()

        self.tolerance_judgment_frame.pack(side=tk.TOP)

        # Units #####
        self.units_frame = tk.Frame(self.parameter_frame)
        # metric button
        self.mm_button = tk.Button(self.units_frame, text='mm', command=self.mm_button_pressed, height=2, width=6)
        self.mm_button.pack(side=tk.LEFT)
        # inch button
        self.inch_button = tk.Button(self.units_frame, text='inch', command=self.inch_button_pressed, height=2, width=6)
        self.inch_button.pack(side=tk.LEFT)
        self.units_frame.pack()

        if self.read_units() =="IN":
            self.inch_button.config(relief=tk.SUNKEN)
            self.mm_button.config(relief=tk.RAISED)
        else:
            self.mm_button.config(relief=tk.SUNKEN)
            self.inch_button.config(relief=tk.RAISED)

    # Main Loop
        self.main_window.after(2000, _thread.start_new_thread, self.get_IDH_data, ())
        # self.main_window.after(2000, _thread.start_new_thread, self.GetIDHData, ())

        tk.mainloop()

    def write_parameter_and_read_return(self, command):
        self.lock.acquire()
        ser.flush()
        ser.write(command)
        return_val = ser.readline()
        self.lock.release()
        return return_val

    def read_gage(self):
        return_val = ser.readline()
        reading = ''
        truereturn = ''
        for byte in return_val:
            truereturn += chr(byte)
        for byte in return_val[5:15]:
            reading += chr(byte)
        try:
            if reading[:4] == "Error":
                print(reading)
                if reading[6:7] == '95':
                    print(errors[reading[6:8]])
                else:
                    print(errors[reading[6:7]])
            else:
                return reading
        except Exception as inst:
            print('Return ' + truereturn)
            print(type(inst))  # the exception instance
            print(inst.args)  # arguments stored in .args
            print(inst)  # __str__ allows args to be printed directly,
            # but may be overridden in exception subclasses
            # x, y = inst.args  # unpack args
            # print('x =', x)
            # print('y =', y)

    def set_zero(self):
        self.write_parameter_and_read_return(set_zero_command)
        print("Wrote Set Zero Cmd")

    def get_IDH_data(self):
        while True:
            return_val = self.write_parameter_and_read_return(read_data_command)
            # ser.flush()
            # ser.write(read_data_command)
            # return_val = ser.readline()
            reading = ''
            truereturn = ''
            for byte in return_val:
                truereturn += chr(byte)
            for byte in return_val[5:15]:
                reading += chr(byte)
            # if reading[:4] == "Error":
            #     print(reading)
            #     if reading[6:7] == '95':
            #         print(errors[reading[6:8]])
            #     else:
            #         print(errors[reading[6:7]])
            # else:
            self.data_value.set(reading)
            try:
                if float(self.current_lower_limit.get()) < float(reading) < float(self.current_upper_limit.get()) \
                        or self.current_tolonoff.get() == "OFF":
                    self.data_value_label.configure(bg='Green')
                else:
                    self.data_value_label.configure(bg='Red')
            except Exception as inst:
                print('partial Return: ' + reading)
                print('Full Return ' + truereturn)
                print(type(inst))  # the exception instance
                print(inst.args)  # arguments stored in .args
                print(inst)  # __str__ allows args to be printed directly,
                    # but may be overridden in exception subclasses
                # x, y = inst.args  # unpack args
                # print('x =', x)
                # print('y =', y)

    def send_tol(self, judgment, upper, lower):
        ser.write(bytes(('DJ' + port_baud[2] + ',' + judgment + '\r\n').encode("ascii")))
        self.current_tolonoff.set(self.new_tolonoff.get())
        print("sent tolerance judgment ON/OFF")
        print('DJ' + port_baud[2] + ',' + judgment + '\r\n')
        if judgment == "ON":
            ser.write(bytes(('CG' + port_baud[2] + ',' + upper + '\r\n').encode("ascii")))
            self.current_upper_limit.set(self.new_upper_limit.get())
            print('wrote upper limit')
            print('CG' + port_baud[2] + ',' + upper + '\r\n')
            ser.write(bytes(('CD' + port_baud[2] + ',' + lower + '\r\n').encode("ascii")))
            self.current_lower_limit.set(self.new_lower_limit.get())
            print('wrote lower limit')
            print('CD' + port_baud[2] + ',' + lower + '\r\n')

    def read_upper_limit(self):
        print("initiated read_upper_limit")
        return_val = self.write_parameter_and_read_return(read_upper_limit_command)
        reading = ''
        truereturn = ''
        for byte in return_val:
            truereturn += chr(byte)
        for byte in return_val[5:15]:
            reading += chr(byte)
        # if reading[:4] == "Error":
        #     if reading[6:7] == '95':
        #         print(errors[reading[6:8]])
        #     else:
        #         print(errors[reading[6:7]])
        # else:
        print('Return ' + truereturn)
        try:
            print(reading)
            # return float(reading)
            return reading
        except Exception as inst:
            print(type(inst))  # the exception instance
            print(inst.args)  # arguments stored in .args
            print(inst)  # __str__ allows args to be printed directly,
                        # but may be overridden in exception subclasses
            # x, y = inst.args  # unpack args
            # print('x =', x)
            # print('y =', y)

    def read_lower_limit(self):
        print("initiated read_lower_limit")
        return_val = self.write_parameter_and_read_return(read_lower_limit_command)
        reading = ''
        truereturn = ''
        for byte in return_val:
            truereturn += chr(byte)
        for byte in return_val[5:15]:
            reading += chr(byte)
        # if reading[:4] == "Error":
        #     if reading[6:7] == '95':
        #         print(errors[reading[6:8]])
        #     else:
        #         print(errors[reading[6:7]])
        # else:
        print('Return ' + truereturn)
        try:
            print(reading)
            # return float(reading)
            return reading
        except Exception as inst:
            print(type(inst))  # the exception instance
            print(inst.args)  # arguments stored in .args
            print(inst)  # __str__ allows args to be printed directly,
                        # but may be overridden in exception subclasses
            # x, y = inst.args  # unpack args
            # print('x =', x)
            # print('y =', y)

    def get_tolonoff(self):
        print("initiated get_tolonoff")
        return_val = self.write_parameter_and_read_return(read_judgment_command)
        reading = ''
        truereturn = ''
        for byte in return_val:
            truereturn += chr(byte)
        for byte in return_val[5:15]:
            reading += chr(byte)
        # if reading[:4] == "Error":
        #     if reading[6:7] == '95':
        #         print(errors[reading[6:8]])
        #     else:
        #         print(errors[reading[6:7]])
        # else:
        try:
            print("whole return: " + truereturn)
            print("partial return: " + truereturn[6:9])
            return truereturn[6:8]
        except Exception as inst:
            print('Return ' + truereturn)
            print(type(inst))  # the exception instance
            print(inst.args)  # arguments stored in .args
            print(inst)  # __str__ allows args to be printed directly,
                        # but may be overridden in exception subclasses
            # x, y = inst.args  # unpack args
            # print('x =', x)
            # print('y =', y)

    def read_units(self):
        print("initiated read_units")
        print(self.write_parameter_and_read_return(read_units_command)[5:7])


    def mm_button_pressed(self):
        self.write_parameter_and_read_return(set_units_mm_command)
        print("wrote: " + 'DU' + port_baud[2] + ',MM')
        print("Units Changed to mm")
        self.mm_button.config(relief=tk.SUNKEN)
        self.inch_button.config(relief=tk.RAISED)
        upper_limit = self.read_upper_limit()
        self.current_upper_limit.set(upper_limit)
        self.new_upper_limit.set(upper_limit)
        print("set upper limit")
        lower_limit = self.read_lower_limit()
        self.current_lower_limit.set(lower_limit)
        self.new_lower_limit.set(lower_limit)
        print("set lower limit")

    def inch_button_pressed(self):
        self.write_parameter_and_read_return(set_units_inch_command)
        print("wrote: " + 'DU' + port_baud[2] + ',IN')
        print("Units Changed to inch")
        self.inch_button.config(relief=tk.SUNKEN)
        self.mm_button.config(relief=tk.RAISED)
        upper_limit = self.read_upper_limit()
        self.current_upper_limit.set(upper_limit)
        self.new_upper_limit.set(upper_limit)
        print("set upper limit")
        lower_limit = self.read_lower_limit()
        self.current_lower_limit.set(lower_limit)
        self.new_lower_limit.set(lower_limit)
        print("set lower limit")

    def set_analog_range(self, range):
        ser.write(bytes(('DR' + port_baud[2] + ',A' + range + '\r\n').encode("ascii")))
        print("wrote" + 'DR' + port_baud[2] + ',A' + range)

gui = Menu()
ser.close()
