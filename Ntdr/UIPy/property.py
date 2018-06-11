class Property(object):
    __slots__ = [
        "width_band",
        "interval" ,
        "routing_parameters"
    ]

    def __init__(self, *, width_band, interval, routing_parameters):
        self.width_band = width_band
        self.interval = interval
        self.routing_parameters = routing_parameters
