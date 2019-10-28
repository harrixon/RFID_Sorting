"""
DENSO

AT10Q-SM 2D barcode reader

Config
1. port         @string     "ttyACM0
2. baudrate     @int        38400
3. timeout      @int        0

Single Read:
1. set time out, since there is no EOL trigger
2. use readline()
3. press trigger on reader to scan
"""

import sys
import time
import serial

# port ID by cmd `ls /dev/serial/by-id/`
defaultPortID = "usb-DENSO_WAVE_INC._USB_Device-if00"

class BarcodeReader:
    def __init__(self, port = "/dev/serial/by-id/" + defaultPortID, baudrate = 38400, timeout = 0):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = serial.Serial()
        self.isActiveReading = False

    # After recognition of the virtual COM port when the USB-COM interface is used, 
    # the scanner requires a maximum of one second to be ready to receive control commands.
    __command_dict__ = {
        # LEDs, return None
        "LED_BLUE": "LB",
        "LED_RED": "LR",
        "LED_GREEN": "LG",
        # Get version, IDs
        "GET_VER": "VER",
        "GET_ID": "ID",
        # Trigger switch on/off
        "TRIGGER_ON": "TMON",
        "TRIGGER_OFF": "TMOFF",
        # Trigger mode
        "MODE_AUTO_OFF": "U1",
        "MODE_MOMENTARY": "U2",     # press n hold to scan, release to standby
        "MODE_ALTERNATE": "U3",     # press to toggle ready n standby
        "MODE_CONT_READ_1": "U4",   # power on > LED on > ready, ignore trigger btn, control by `Z`or`R` cmd
        "MODE_CONT_READ_2": "U5",   # same as above, except wait for cmd upon scan complete
        "MODE_AUTO_SENSE": "U6",
        # save U1-U6 settings in EEPROM to prevent lost after device power off
        "MODE_SAVE": "PW",
        # U4, U5 control, also require STX header 0x02
        "MODE_CONT_STANDBY": "Z",
        "MODE_CONT_READY": "R"
    }

    def __command__(self, cmd):
        # default
        header = b""
        eol = b"\r\n"
        return header + str.encode(self.__command_dict__[cmd]) + eol

    def __byte_list_to_str__(self, byteList):
        return "".join([bytes.decode(x) for x in byteList])

    def __open_port__(self):
        if self.ser.isOpen():
            print("Port %s is already open, check your code" % self.ser.port)
        else:
            # serial port settings
            self.ser.port = self.port
            self.ser.baudrate = self.baudrate
            self.ser.timeout = self.timeout
            print("Port opening with config:")
            print("port: ", self.ser.port)
            print("baudrate: ", self.ser.baudrate)
            print("timeout: ", self.ser.timeout)
            # open
            self.ser.open()

    def __terminate_port__(self):
        if self.ser.isOpen():
            print("Closing port")
            self.ser.close()

    def __read_on_press__(self):
        # single read mode has no EOL on output data, only `\r`, ie no `readline()`
        # solution : loop with `read()`
        # How to use: run this function > press trigger on scanner > scan a code

        # open port
        self.__open_port__()

        # var that contains read in data
        data = []
        keepReading = True
        
        try:
            while self.ser.isOpen() and keepReading:
                charIn = self.ser.read(1)
                
                if len(data) == 0:
                    if charIn:
                        # data starts to come in
                        data.append(charIn)
                else:
                    if (charIn == b"\r" or charIn == b"\n" or charIn == b""):
                        # data stops coming in, kill
                        keepReading = False
                    else:
                        # data keeps coming in
                        data.append(charIn)

        except:
            print("Unexpected error:", sys.exc_info())
            data = []
        
        finally:
            self.__terminate_port__()

        data = self.__byte_list_to_str__(data)
        return data

    def __start_continuous_read__(self, cb):
        """
        Function
        Reader is set to ready state, ie READ at any time
        Once a code is read, reader is set to stand-by state
        Takes a callback fucntion to return data

        Code logic
        1. Open port
        2. Set cont read mode 1
            a. scanner starts scanning, feeds back b''
        3. Upon successful read
            a. change state to standby, send "stand by" cmd to scanner
            b. emit received data to main program
        4. Receive ok from main program, turn scanner to "ready"
            a. Back to step 2.a
        """

        # 0
        self.isActiveReading = True
        rawData = b''

        # 1
        self.__open_port__()

        # 2
        try:
            while self.ser.isOpen() and self.isActiveReading:
                # 2a
                # set reading mode, start reading
                self.ser.write(self.__command__("MODE_CONT_READ_1"))

                # 3a
                # scanner reading, catch input, isActiveReading = F
                rawData = self.__reading_loop__()
                print("First Successful Reading:")
                print(rawData)
                print("======")

                # 3b
                cb(rawData)

        except KeyboardInterrupt as err:
            # self.__is_port_open__("crtl c")
            print("\nBarcode Reader: KeyboardInterrupt")
            self.__standby_n_exit__()
        except SystemExit as err:
            # self.__is_port_open__("sys")
            print("\nBarcode Reader: SystemExit: ", err)
            self.__standby_n_exit__()
        finally:
            # self.__is_port_open__("finally")
            self.__set_scanner_standby__()

        return

    def __next_read__(self, cb):
        self.__set_scanner_ready__()
        rawData = self.__reading_loop__()
        print(rawData)
        print("======")
        cb(rawData)
        return

    def __set_scanner_ready__(self):
        self.isActiveReading = True
        if self.ser.isOpen():
            print("Set scanner ready")
            self.ser.write(self.__command__("MODE_CONT_READY"))
            time.sleep(1)   # max 1s to process cmd
        return

    def __set_scanner_standby__(self):
        self.isActiveReading = False
        if self.ser.isOpen():
            print("Set scanner stand by")
            self.ser.write(self.__command__("MODE_CONT_STANDBY"))
            time.sleep(1)   # max 1s to process cmd
        return

    def __reading_loop__(self):
        rawData = b''
        if self.ser.isOpen():
            while self.isActiveReading:
                try:
                    rawData = self.ser.readline()
                    if rawData != b'':
                        self.isActiveReading = False
                        self.__set_scanner_standby__()
                except Exception as e:
                    self.__is_port_open__("reading loop")
                    print("reading loop: ", e)
                    self.__standby_n_exit__()
        return rawData

    def __standby_n_exit__(self):
        # self.__is_port_open__("quit")
        print("Exiting")
        if self.ser.isOpen():
            self.__set_scanner_standby__()
            self.__terminate_port__()
        return

    # debug
    def __is_port_open__(self, txt):
        print("At ", txt, " is port still open? ", self.ser.isOpen())