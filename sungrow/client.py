from pymodbus.client import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
import struct
import logging
logger = logging.getLogger(__name__)

from sungrow.server import Server

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
        # maybe inherit modbusclient

    def connect(self):
        self.client.connect()

    def close(self):
        self.client.close()

    ###########################
    # move to server-specific
    def _decoded(content, dtype):
        #TODO see convert from registers
        if dtype == "UTF-8": return _decode_utf8(content)
        elif dtype == "U16": return _decode_u16(content)
        elif dtype == "U32": return _decode_u32(content)
        elif dtype == "S16": return _decode_s16(content)
        elif dtype == "S32": return _decode_s32(content)
        else: raise NotImplementedError(f"Data type {dtype} decoding not implemented")

    def _decode_u16(registers):
        """ Unsigned 16-bit big-endian to int """
        return registers[0]
    
    def _decode_s16(registers):
        """ Signed 16-bit big-endian to int """
        return ModbusSerialClient.convert_from_registers(registers=registers, data_type=ModbusSerialClient.DATATYPE.INT16)

    def _decode_u32(registers):
        """ Unsigned 32-bit mixed-endian word"""
        packed = struct.pack('>HH', registers[1], registers[0])
        return struct.unpack('>I', packed)[0]
    
    def _decode_s32(registers):
        """ Signed 32-bit mixed-endian word"""
        # return ModbusSerialClient.convert_from_registers(registers=registers, data_type=ModbusSerialClient.DATATYPE.INT32)
        packed = struct.pack('>HH', registers[1], registers[0])
        return struct.unpack('>i', packed)[0]

    def _decode_utf8(registers):
        return ModbusSerialClient.convert_from_registers(registers=registers, data_type=ModbusSerialClient.DATATYPE.STRING)
    ###########################3

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

        return _decoded(result.registers)*multiplier

    def write_register(self, register_name: str):
        pass

    def from_config(client_cfg: dict, connection_specs: dict):
        conection_cfg = connection_specs[client_cfg["connection_specs"]]
        
        return ModbusRtuClient(client_cf["name"], client_cfg["nickname"], client_cfg["port"], 
                            connection_cfg["baudrate"], connection_cfg["bytesize"], 
                            connection_cfg["parity"], connection_cfg["stopbits"])

    def __str__(self):
        return f"{self.nickname}"


if __name__ == "__main__":
    # # Test Decoding
    # mock_u16_register = [258, ]                     # 0x0102 -> 258
    # mock_u32_register = [772, 258]                  # 0x01020304 -> 16909060
    mock_utf8_register = [16706, 17220, 17734, 18248, 18762]
    mock_s16_register = [32768]                     #2*15 == -32767
    mock_s16_register2 = [2**16-1]                     #2*16-1 == -1
    mock_s32_register = [65535, 65535]                     #2*32-1 == -1
    mock_s32_register2 = [30587, 65535]                     # 0xFFFF777B -> -34949 
    
    # print(ModbusRtuClient._decode_u16(mock_u16_register))
    # print(ModbusRtuClient._decode_u32(mock_u32_register))
    print(ModbusRtuClient._decode_utf8(mock_utf8_register))
    print(ModbusRtuClient._decode_s16(mock_s16_register))
    print(ModbusRtuClient._decode_s16(mock_s16_register2))
    print(ModbusRtuClient._decode_s32(mock_s32_register))
    print(ModbusRtuClient._decode_s32(mock_s32_register2))

