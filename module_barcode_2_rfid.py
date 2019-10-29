from util_barcode_reader import BarcodeReader
from util_rdif_writer import RFIDWriter

import re

class Barcode2RFID:
    def __init__(self):
        self.reader = BarcodeReader()
        self.writer = RFIDWriter()
        self.reading = True

    def __run__(self):
        try:
            print("B2R: Start")
            self.reader.__start_continuous_read__(self.__on_receive__)

        except Exception as e:
            print("B2R: ", e)
            self.reader.__standby_n_exit__()

    def __on_receive__(self, data):
        # check if received data is HA ticket
        ticket = ""
        if type(data) is bytes:
            ticket = bytes.decode(data).strip()
            self.__validate_ticket__(ticket)
        elif type(data) is str:
            ticket = data.strip()
            self.__validate_ticket__(ticket)
        else:
            print("Data type neither byte nor string, please check scanner setting")
            self.reader.__standby_n_exit__()

    def __validate_ticket__(self, ticket):
        print("B2R: Incoming data: %s" % ticket)
        
        """
        ticket string format
        1. 13 <= length <= 16
        2. [:8] is DDMMYYYY
        3. [8:12] is ticket id, eg: 0001
        4. [12:] is item id on ticket, eg: 1, 12, 333; max len = 4
        """
        isValid = bool
        if len(ticket) < 13 or len(ticket) > 16:
            print("Invalid length, min 13, max 16, received: ", len(ticket))
            isValid = False
        elif not re.match(r"^([0-2][0-9]|(3)[0-1])(((0)[0-9])|((1)[0-2]))\d{4}$", ticket[:8]):
            print("Invalid date format, should be DDMMYYYY, received: ", ticket[:8])
            isValid = False
        elif not re.match(r"^\d{4}$", ticket[8:12]):
            print("Invalid ticket id, should be 4 digits with starting zeros, received: ", ticket[8:12])
            isValid = False
        elif not re.match(r"^\d{1,4}$", ticket[12:]):
            print("Invalid item id, min 1 digi, max 4 digits, received : ", ticket[12:])
            isValid = False
        else:
            isValid = True

        if isValid:
            print("B2R: Valid Ticket, write 2 Tag\n======")
            # TODO: GREEN LED to signal ok
            self.__write_2_RFID__(ticket)
        else:
            # read again
            print("B2R: Invalid ticket, next read\n======")
            # TODO: RED LED to signal fail
            self.reader.__next_read__(self.__on_receive__)

    def __write_2_RFID__(self, ticket):
        print("Write 2 RFID")
        pass
        # success = self.writer.__write__(ticket)

        # if not success:
        #     print("B2R: Write to RFID error\n======")
        # else:
        #     print("B2R: Write to RFID success\n======")

  
