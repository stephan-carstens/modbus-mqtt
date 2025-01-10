import unittest
from sungrow.sungrow_inverter import SungrowInverter

class TestSungrowInverter(unittest.TestCase):

    # def setUp(self):
    #     self.inverter = SungrowInverter()

    def test_decode_u16(self):
        # 0x0102 -> 258
        self.assertEqual(SungrowInverter._decode_u16([258, ]), 258)      

    def test_decode_u32(self):
        # 0x01020304 -> 16909060
        self.assertEqual(SungrowInverter._decode_u32([772, 258]), 16909060)      