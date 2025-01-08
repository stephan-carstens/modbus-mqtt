import json
import os

class ConfigLoader:
    def __init__(self):
        self.servers = []
        self.clients = []
        pass

    def load(filename):
        if os.path.exists(filename):
            with open("data/options.json") as f:
                data = json.load(f)

                # save data 

        return ConfigLoader()
