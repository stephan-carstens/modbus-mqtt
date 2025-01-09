import json
import os


class ConfigLoader:
   
    @staticmethod
    def load(json_rel_path) -> tuple[dict, dict]:
        """ Load server, client configurations and connection specs as dicts from options json. """

        if os.path.exists(json_rel_path):
            with open(json_rel_path) as f:
                data = json.load(f)
        else:
            raise FileNotFoundError(f"Config options json not found.")

        cls.validate(data)

        return data["servers"], data["clients"], data["connection_specs"]

    @staticmethod
    def validate(data):
        pass

# Option schema example
# {'options': {'clients': [{'name': 'usb_to_modbus',
#     'nickname': 'Client1',
#     'connectionspecs': 'SunGrow Inverter'}],
#   'servers': [{'name': 'SunGrow Inverter 1',
#     'serialnum': '12345678',
#     'nickname': 'SG1',
#     'server_type': 'SunGrow Inverter'}]}}