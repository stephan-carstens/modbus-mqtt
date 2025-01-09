class SungrowInverter(Server):
    output_types = ["Two Phase", "3P4L", "3P3L"]

    self.sensors = None
    # {
        # "Serial Number":        {"addr": 4990, "dtype": "UTF-8", "multiplier": 1, "unit": ""},
        # "Device Type Code":     {"addr": 5000, "dtype": "U16", "multiplier": 1, "unit": ""},
        # "Nominal Active Power": {"addr": 5001, "dtype": "U16", "multiplier": 0.1, "unit": "kW"},
        # "Output Type":          {"addr": 5002, "dtype": "U16", "multiplier": 1, "unit": ""},
        # "Daily Power Yields":   {"addr": 5003, "dtype": "U16", "multiplier": 0.1, "unit": "kWh"},
        # "Total Power Yields":          {"addr": 5004, "dtype": "U16", "multiplier": 0.1, "unit": "kWh"},
        # TODO
    # }