from pymodbus.client import ModbusSerialClient
import struct

from server import Server

DEBUG = True
def debug(content):
    if DEBUG: print(content)

class ModbusRtuClient:
    def __init__(self, name, nickname, port, baudrate, bytesize=8, parity=false, stopbits=1, timeout=1):
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

    def read_register(self, server:Server, sensor:Sensor):
        """ Read an individual register using pymodbus """

        register = sensor.name
        address = sensor.addr
        dtype = sensor.dtype
        multiplier = sensor.multiplier
        unit = register["unit"]

        result = self.client.read_holding_registers(address-1)  # slave id TODO

        if result.isError():
            raise Exception(f"Error reading register {register_name}")

        return _decoded(result)*multiplier

    def write_register(self, register_name: str):
        pass

    def from_config(client_cfg: dict, connection_specs: dict) -> Client:
        conection_cfg = connection_specs[client_cfg["connection_specs"]]
        
        return ModbusRtuClient(client_cf["name"], client_cfg["nickname"], client_cfg["port"], 
                            connection_cfg["baudrate"], connection_cfg["bytesize"], 
                            connection_cfg["parity"], connection_cfg["stopbits"])

    def __str__(self):
        return f"{self.nickname}"


if __name__ == "__main__":
    # Test Decoding
    # 0x0102 -> 258
    print(ModbusRtuClient._decode_u16([0x01, 0x02]))
    # print(convert_from_registers([0x0102], ))
    # 0x01020304 -> 16909060
    print(ModbusRtuClient._decode_u32([0x03, 0x04, 0x01, 0x02]))
    # print(_decode_utf_8())
