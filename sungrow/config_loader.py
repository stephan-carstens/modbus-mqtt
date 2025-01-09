import json
import os

class ConfigLoader:
    def __init__(self, servers, clients):
        self.servers = []
        self.client = None
        pass

    def load():
        if os.path.exists("data/options.json"):
            with open("data/options.json") as f:
                data = json.load(f)
        else:
            raise FileNotFoundError(f"options.json not found")

        # save data 
        client = data["clients"][0]      # suport 1 client only 0.1.0
        servers = data["servers"]

        return ConfigLoader(servers, client)


# {'options': {'clients': [{'name': 'usb_to_modbus',
#     'nickname': 'Client1',
#     'connectionspecs': 'SunGrow Inverter'}],
#   'servers': [{'name': 'SunGrow Inverter 1',
#     'serialnum': '12345678',
#     'nickname': 'SG1',
#     'server_type': 'SunGrow Inverter'}]}}