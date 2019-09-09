class IDOutletMapping:
    def __init__(self):
        # "outlet_id" : "ticket_id"
        self.map_object = {
            "1": None,
            "2": None,
            "3": None,
            "4": None
        }

    def __main__(self):
        pass

    """
        __lookup_w_id__
            :arg    @string ticket_id
            :return @string outlet_id
    """
    def __lookup_w_id__(self, ticket_id):
        # return outlet_id (key) if found
        # else return None
        pass

    """
        __delete_mapping__
            :arg    @string ticket_id
            :return @None
    """
    def __delete_mapping__(self, ticket_id):
        pass

    """
        __add_mapping__
            :arg    @string ticket_id
            :return @string outlet_id
    """
    def __add_mapping__(self, ticket_id):
        # return outlet_id (key)
        pass

    """
        __slot_available__
            :arg    @None
            :return @string outlet_id
    """
    def __slot_available__(self):
        pass
