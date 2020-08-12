class RFIDWriter:
    # port ID by cmd `ls /dev/serial/by-id/`
    __defaultPortID__ = "usb-1a86_USB2.0-Serial-if00-port0"

    def __init__(self):
        pass

    def __main__(self):
        return "pass"

    def __write__(self, ticket):
        return "pass"
