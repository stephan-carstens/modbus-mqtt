from pymodbus.client import ModbusSerialClient
import struct

from server import Server

DEBUG = True
def debug(content):
    if DEBUG: print(content)

class ModbusComm:
    def __init__(self, server:Server, port):
        self.server = None
        self.client = ModbusSerialClient(method='rtu', port=port, baudrate=9600, timeout=1)

    def connect(self):
        self.client.connect()

    def close(self):
        self.client.close()

    def _decoded(content, dtype):
        #TODO see convert from registers
        if dtype == "UTF-8": return _decode_utf8(content)
        elif dtype == "U16": return _decode_u16(content)
        elif dtype == "U32": return _decode_u32(content)
        else: raise NotImplementedError(f"Data type {dtype} decoding not implemented")

    def _decode_u16(content):
        """ Unsigned 16-bit big-endian to int"""
        packed = struct.pack('>HBB', 0x0000, content[0], content[1])
        debug(packed)
        return struct.unpack('<I', packed)

    def _decode_u32(content):
        """ Unsigned 32-bit little-endian word"""
        packed = struct.pack('<HH', content[1], content[0])
        debug(packed)
        return struct.unpack('<I', packed)

    def _decode_utf8(content):
        packed = struct.pack('')

    def read_register(self, register_name: str):
        """ Read an individual register using pymodbus """

        register = self.register_map[register_name]

        address = register["addr"]
        dtype = register["dtype"]
        multiplier = register["multiplier"]
        unit = register["unit"]

        result = self.client.read_holding_registers(address-1)  # slave id TODO

        if result.isError():
            raise Exception(f"Error reading register {register_name}")

        return _decoded(result)*multiplier

    def write_register(self, register_name:str):
        pass

if __name__ == "__main__":
    # Test Decoding
    # 0x0102 -> 258
    print(ModbusComm._decode_u16([0x01, 0x02]))
    # print(convert_from_registers([0x0102], ))
    # 0x01020304 -> 16909060
    print(ModbusComm._decode_u32([0x03, 0x04, 0x01, 0x02]))
    # print(_decode_utf_8())
