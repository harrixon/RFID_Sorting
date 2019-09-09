from util_barcode_reader import BarcodeReader
from util_rdif_writer import RFIDWriter


class Barcode2RFID:
    def __init__(self):
        self.reader = BarcodeReader.__init__()
        self.writer = RFIDWriter.__init__()

    def __run__(self):
        try:
            while True:
                #  probably need to await
                ticket = self.reader.__read__()

                if ticket:
                    #  probably need to await
                    self.writer.__write__(ticket)

        except InterruptedError as e:
            # maybe also reset / stop reader / writer
            print(e)

