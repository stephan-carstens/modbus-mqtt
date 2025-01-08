from config_loader import ConfigLoader

class Server:
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
            pass
    
    self.nickname: str = None
    self.serialnum: str = None
    self.connected_client = None
    self.sensors: list[Sensor] = []

    def from_config(config_loader: ConfigLoader) -> Server:
        pass

