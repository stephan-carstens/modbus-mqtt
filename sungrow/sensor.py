class Sensor:
    def __init__(self, name, addr, dtype, multiplier, unit):
        self.name = name
        self.addr = addr
        self.dtype = dtype
        self.multiplier = multiplier
        self.unit = unit

    @property
    def value():
        pass

    def publish():
        # todo separate from sensor into mqtt_helper
        pass