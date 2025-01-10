import unittest
from sungrow.client import ModbusRtuClient

class TestClient(unittest.TestCase):

    def setUp(self):
        self.client = ModbusRtuClient("Test", "T", 8080, 9600, 8, False, 1, 1)

    def test_decode_u16(self):
        # 0x0102 -> 258
        self.assertEqual(ModbusRtuClient._decode_u16([258, ]), 258)      

    def test_decode_u32(self):
        # 0x01020304 -> 16909060
        self.assertEqual(ModbusRtuClient._decode_u32([772, 258]), 16909060)      