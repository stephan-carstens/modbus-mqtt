from sungrow.config_loader import ConfigLoader
import abc

class Server(metaclass=abc.ABCMeta):

    
    def __init__(self, name:str, nickname:str, serialnum:str, connected_client):
        self.name = name
        self.nickname= nickname
        self.serialnum = serialnum
        self.connected_client = connected_client
        self.registers: list = []
        self.manufacturer:str | None = None
        self.model:str | None = None
        # self.isConnected: bool = False
        # self.batches TODO

    def verify_serialnum(self, serialnum_as_read:str):
        if self.serialnum is None: raise ConnectionError(f"Failed to read serialnum of {self.nickname}.")
        elif self.serialnum != serialnum_as_read: raise ValueError(f"Mismatch in configured serialnum {self.serialnum} \
                                                                        and actual serialnum {serialnum_as_read} for server {self.nickname}.")

    def batchify_registers(self):
        pass

    def from_config(server_cfg:dict, clients:list):
        # assume valid configLoader object
        try:
            idx = [str(client) for c in clients].index(server_cfg["connected_client"])  # TODO ugly
        except:
            raise ValueError(f"Client {server_cfg['connected_client']} from server {server_cfg['nickname']} config not defined in client list")

        return Server(server_cfg["name"], server_cfg["nickname"], server_cfg["serialnum"], connected_client=clients[idx])

    @abc.abstractmethod
    def _decoded(content):
        raise NotImplementedError("Server-specific decoding must be implemented.")
