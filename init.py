"""
    This project uses RFID technology to identify and sort packaged drug coming from drug shelf,
    before professional personnel verify the competence of a prescript.

    Steps:

    1.  Retrieve patient ticket id on each drug package label with barcode scanner
    2.  Use the retrieved ticket id to generate a RFID tag, apply the tag on the package
    3.  Tagged packages travels along conveyor belt and reaches RFID scanner
    4.  RFID scanner reads the tag on the package, identify patient ticket id
    5.  Assign corresponding outlet for package according to ticket id

    Barcode Converter
    - directly copy the string from barcode to RFID tag
        
        1D barcode Reading
            :arg    None
            :return @string full_ticket_id
        
        RFID writer 
            :arg    @string full_ticket_id
            :return null

    Sorting Machine
    - read full ticket id from tag
    - map ticket id to outlet
        - slice last 2 digits from id (item number on that ticket, useless)
        - lookup, delete, add
    - open up outlet according to id obtained
    
    
        RFID reader
            :arg    None
            :return @string full_ticket_id
            
        id-outlet-mapping
            :arg    @string ticket_id
            :return @string outlet_id
            
        outlet control
            :arg    @string outlet_id
            :return None
    
"""

from multiprocessing import Process
from module_barcode_2_rfid import Barcode2RFID
from module_sort_and_assign import SortAndAssign


def process_one():
    # barcode_2_rfid = Barcode2RFID()
    # barcode_2_rfid.run()
    pass


def process_two():
    # sort_and_assign = SortAndAssign()
    # sort_and_assign.run()
    pass


def __main__():
    try:
        # 2 standalone processes
        p1 = Process(target=process_one, args=())
        p2 = Process(target=process_two, args=())

        p1.start()
        p2.start()

        p1.join()
        p2.join()

    finally:
        print("Process Terminated")

