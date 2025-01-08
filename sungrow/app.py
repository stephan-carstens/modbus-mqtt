""" TODO pseudocoe for the main application """

from modbus_com import ModbusComm
from config_loader import ConfigLoader
from time import sleep

# Read configuration
config = ConfigLoader.load()

# Instantiate clients (modbus adapters)
comm = ModbusComm(port=config.port)     # support 1 client 0.1.0
comm.connect()

# Instantiate servers
servers = []

# every read_interval seconds, read the registers and publish to mqtt
while True:
    for inverter_cfg in config.servers:
        for register_name in inverter_cfg.registers:
            value = comm.read_register(inverter_cfg, register_name)
            inverter_cfg.publish(register_name, value)

    sleep(config.read_interval)

comm.close()
