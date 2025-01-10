from pymodbus.client import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder
# from pymodbus.constants import Endian
import struct
import logging
logger = logging.getLogger(__name__)

from server import Server

DEBUG = True
def debug(content):
    if DEBUG: print(content)

class ModbusRtuClient:
    def __init__(self, name, nickname, port, baudrate, bytesize=8, parity=False, stopbits=1, timeout=1):
        self.name = name
        self.nickname = nickname
        self.client = ModbusSerialClient(   port=port, baudrate=baudrate, 
                                            bytesize=bytesize, parity=parity, stopbits=stopbits, 
                                            timeout=timeout)


    def read_register(self, server:Server, register_name:str, register_info:dict):
        """ Read an individual register using pymodbus """

        # register = register["name"]
        address = register_info["addr"]
        dtype =  register_info["dtype"]
        multiplier = register_info["multiplier"]
        unit = register_info["unit"]

        result = self.client.read_holding_registers(address-1)  # slave id TODO
        # result.registers

        if result.isError():
            raise Exception(f"Error reading register {register_name}")

        return server._decoded(result.registers)
        return _decoded(result.registers)*multiplier
        # TODO multiplier

    def write_register(self, register_name: str):
        pass

    def connect(self):
        self.client.connect()

    def close(self):
        self.client.close()

    def from_config(client_cfg: dict, connection_specs: dict):
        conection_cfg = connection_specs[client_cfg["connection_specs"]]
        
        return ModbusRtuClient(client_cf["name"], client_cfg["nickname"], client_cfg["port"], 
                            connection_cfg["baudrate"], connection_cfg["bytesize"], 
                            connection_cfg["parity"], connection_cfg["stopbits"])

    def __str__(self):
        return f"{self.nickname}"
