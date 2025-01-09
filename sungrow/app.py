from time import sleep

from config_loader import ConfigLoader
from client import ModbusRtuClient as Client
from server import Server
from sungrow_inverter import SungrowInverter

try:
    # Read configuration
    servers_cfgs, clients_cfgs, connection_specs = ConfigLoader.load()

    # Instantiate clients (modbus adapters)
    clients = [Client.from_config(client_cfg, connection_specs) for client_cfg in clients_cfgs]
    # Instantiate servers
    servers = [SungrowInverter.from_config(server_cfg, comm) for server_cfg in servers_cfgs]

    # every read_interval seconds, read the registers and publish to mqtt
    while True:
        for server in servers:
            for register in server.registers:
                client = server.connected_client
                value = client.read_register(server, register)
                mqtt_helper.publish(register, value)

        sleep(config.read_interval)
finally:
    for client in clients:
        client.close()
