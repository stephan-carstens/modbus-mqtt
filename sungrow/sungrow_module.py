from pymodbus.client import ModbusSerialClient
import struct

DEBUG = True
def debug(content):
    if DEBUG: print(content)

class SungrowComm:
    output_types = ["Two Phase", "3P4L", "3P3L"]

    register_map = {
        "Serial Number":        {"addr": 4990, "dtype": "UTF-8", "multiplier": 1, "unit": ""},
        "Device Type Code":     {"addr": 5000, "dtype": "U16", "multiplier": 1, "unit": ""},
        "Nominal Active Power": {"addr": 5001, "dtype": "U16", "multiplier": 0.1, "unit": "kW"},
        "Output Type":          {"addr": 5002, "dtype": "U16", "multiplier": 1, "unit": ""},
        "Daily Power Yields":   {"addr": 5003, "dtype": "U16", "multiplier": 0.1, "unit": "kWh"},
        # "Total Power Yields":          {"addr": 5004, "dtype": "U16", "multiplier": 0.1, "unit": "kWh"},
        # TODO
    }
    
    def __init__(self, port):
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
        register = self.register_map[register_name]

        address = register["addr"]
        dtype = register["dtype"]
        multiplier = register["multiplier"]
        unit = register["unit"]

        result = self.client.read_holding_registers(address-1)  # slave id TODO

        if result.isError():
            raise Exception(f"Error reading register {register_name}")

        return _decoded(result)*multiplier

if __name__ == "__main__":
    # Test Decoding
    # 0x0102 -> 258
    print(SungrowComm._decode_u16([0x01, 0x02]))
    print(convert_from_registers([0x0102], ))
    # 0x01020304 -> 16909060
    print(SungrowComm._decode_u32([0x03, 0x04, 0x01, 0x02]))
    # print(_decode_utf_8())
