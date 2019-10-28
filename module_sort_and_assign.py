from util_rfid_reader import RFIDReader
from util_outlet_controller import OutletController
from id_outlet_mapping import IDOutletMapping


class SortAndAssign:
    def __init__(self):
        self.reader = RFIDReader()
        self.outlet_controller = OutletController(7)
        self.mapping = IDOutletMapping()

    def __process_ticket_id__(self, ticket):
        # last 2 char = item's id on the list, useless
        ticket_id = ticket[:len(ticket) - 2]

        # mapping
        outlet = self.mapping.__lookup_w_id__(ticket_id)

        if outlet:
            return outlet
        else:
            # for demo, there is no deleting, queuing ... etc
            return self.mapping.__add_mapping__(ticket_id)

    def __run__(self):
        pass
        # try:
        #     while True:
        #         #  probably need to await
        #         ticket = self.reader.__read__()

        #         if ticket:
        #             #  probably need to await
        #             outlet = self.__process_ticket_id__(ticket)

        #             if outlet is not None:
        #                 self.outlet_controller.__move_to__(outlet)

        #             else:
        #                 self.outlet_controller.__reset__()
        #                 print("[BUG] outlet value not found")

        # except InterruptedError as e:
        #     # maybe also reset / stop reader / writer
        #     print(e)
            