from util_barcode_reader import BarcodeReader
from util_rdif_writer import RFIDWriter


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
        1. length = 14
        2. [0:7] is DDMMYYYY
        3. [8:11] is ticket id
        4. [12:13] is item id on ticket
        """
        isValid = False

        if isValid:
            print("B2R: Valid Ticket, write 2 Tag\n======")
            self.__write_2_RFID__(ticket)
        else:
            # read again
            print("B2R: Invalid ticket, next read\n======")
            self.reader.__next_read__(self.__on_receive__)

    def __write_2_RFID__(self, ticket):
        pass
        # success = self.writer.__write__(ticket)

        # if not success:
        #     print("B2R: Write to RFID error\n======")
        # else:
        #     print("B2R: Write to RFID success\n======")

  
