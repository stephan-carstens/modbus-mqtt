""" TODO pseudocoe for the main application """

from client import ModbusRtuClient as Client
from config_loader import ConfigLoader
from time import sleep
from server import Server

# Read configuration
servers_cfgs, clients_cfgs, connection_specs = ConfigLoader.load(json_rel_path="data/options.json")

# Instantiate clients (modbus adapters)
clients = [Client.from_config(client_cfg, connection_specs) for client_cfg in clients_cfgs]
# Instantiate servers
servers = [Server.from_config(server_cfg, comm) for server_cfg in servers_cfgs]

# every read_interval seconds, read the registers and publish to mqtt
while True:
    for server in servers:
        for sensor in server.sensors:
            value = comm.read_register(inverter_cfg, register_name)
            inverter_cfg.publish(register_name, value)

    sleep(config.read_interval)

comm.close()
