import serial
import time
import sys
import glob
import tkinter as tk
import pyautogui
import _thread

baud = 2400
cmd = bytes(('1' + '\r\n').encode('ascii'))

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


def port_select(ports):
    master = tk.Tk()

    master['padx'] = 40
    master['pady'] = 40

    port_frame = tk.Frame(master, width=200)

    port_label = tk.Label(port_frame)
    port_label["text"] = "Choose Port"
    port_label.pack(side=tk.LEFT)


    port = tk.StringVar(port_frame)

    # idlabel = tk.Label(master, text="ID Number")

    port.set(ports[0])  # default value

    port_choice = tk.OptionMenu(port_frame, port, *ports)

    port_frame.pack()

    port_choice.pack()

    def ok():
        print("port is", port.get())

        master.destroy()

    button = tk.Button(master, text="OK", command=ok)
    button.pack()

    tk.mainloop()
    return port.get()

port = port_select(serial_ports())

ser = serial.Serial(port=port, baudrate=baud, timeout=1)

class Main_program:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title("Input Tool to RS-232 HID Output")

        self.quitButton = tk.Button(self.main_window, text='Quit', command=self.main_window.destroy, height=2, width=6)
        self.quitButton.pack()
        # self.quitButton.place(x=50, y=500)
        self.main_window.after(2000, _thread.start_new_thread, self.get_data(), ())
        tk.mainloop()

    def get_data(self):
        while True:
            reading = ''
            ser.write(cmd)
            return_val = ser.readline()
            for byte in return_val[3:]:
                reading += chr(byte)
            pyautogui.typewrite(reading + '\n')
            time.sleep(.5)

gui = Main_program()
ser.close()
