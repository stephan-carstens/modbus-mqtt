class SungrowInverter(Server):
    output_types = ["Two Phase", "3P4L", "3P3L"]

    self.registers = [
        {"name": "Serial Number", "addr": 4990, "dtype": "UTF-8", "multiplier": 1, "unit": ""},
        {"name": "Device Type Code" , "addr": 5000, "dtype": "U16", "multiplier": 1, "unit": ""},
        {"name": "Nominal Active Power" , "addr": 5001, "dtype": "U16", "multiplier": 0.1, "unit": "kW"},
        {"name": "Output Type" , "addr": 5002, "dtype": "U16", "multiplier": 1, "unit": ""},
        {"name": "Daily Power Yields", "addr": 5003, "dtype": "U16", "multiplier": 0.1, "unit": "kWh"},
        {"name": "Total Power Yields", "addr": 5004, "dtype": "U16", "multiplier": 0.1, "unit": "kWh"},
    ]