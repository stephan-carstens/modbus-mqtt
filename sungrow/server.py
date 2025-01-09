from config_loader import ConfigLoader
from client import ModbusRtuClient as Client

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
    
    def __init__(self, name, nickname, serialnum, connected_client):
        self.name = name
        self.nickname: str = nickname
        self.serialnum: str = serialnum
        self.connected_client = connected_client
        self.sensors: list[Sensor] = []

    def from_config(server_cfg:dict, clients:list[Client]) -> Server:
        # assume valid configLoader object
        try:
            idx = [str(client) for c in clients].index(server_cfg["connected_client"])  # TODO ugly
        except:
            raise ValueError(f"Client {server_cfg['connected_client']} from server {server_cfg['nickname']} config not defined in client list")

        return Server(server_cfg["name"], server_cfg["nickname"], server_cfg["serialnum"], connected_client=clients[idx])

