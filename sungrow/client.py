from pymodbus.client import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
import struct

from server import Server

DEBUG = True
def debug(content):
    if DEBUG: print(content)

class ModbusRtuClient:
    def __init__(self, name, nickname, port, baudrate, bytesize=8, parity=False, stopbits=1, timeout=1):
        self.name = name
        self.nickname = nickname
        self.client = ModbusSerialClient(   method='rtu', port=port, baudrate=baudrate, 
                                            bytesize=bytesize, paity=parity, stopbits=stopbits, 
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
        else: raise NotImplementedError(f"Data type {dtype} decoding not implemented")

    def _decode_u16(registers):
        """ Unsigned 16-bit big-endian to int """
        return registers[0]
    
    # def _decode_s16(registers):
    #     """ Signed 16-bit big-endian to int """
    #     packed = struct.pack('>hh', 0x0000, registers[0])
    #     return struct.unpack('>I', packed)[0]

    def _decode_u32(registers):
        """ Unsigned 32-bit mixed-endian word"""
        packed = struct.pack('>HH', registers[1], registers[0])
        return struct.unpack('>I', packed)[0]

    def _decode_utf8(registers):
        return ModbusSerialClient.convert_from_registers(registers=registers, data_type=ModbusSerialClient.DATATYPE.STRING)
    ###########################3

    def read_register(self, server:Server, register):
        """ Read an individual register using pymodbus """

        register = register["name"]
        address = register["addr"]
        dtype =  register["dtype"]
        multiplier = register["multiplier"]
        unit = register["unit"]

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
    mock_u16_register = [258, ]                     # 0x0102 -> 258
    mock_u32_register = [772, 258]                  # 0x01020304 -> 16909060
    mock_utf8_register = [16706, 17220, 17734, 18248, 18762]
    # BPD
    # decoder = BinaryPayloadDecoder.fromRegisters(registers=mock_u16_register,
    #                                                 byteorder=Endian.BIG,
    #                                                 wordorder=Endian.BIG)

    # print(decoder.decode_32bit_float())

    
    # Test Decoding
    print(ModbusRtuClient._decode_u16(mock_u16_register))
    # print(convert_from_registers([0x0102], ))
    print(ModbusRtuClient._decode_u32(mock_u32_register))
    # print(_decode_utf_8())
    print(ModbusRtuClient._decode_utf8(mock_utf8_register))

