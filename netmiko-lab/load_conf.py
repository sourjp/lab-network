#!/usr/bin/env python3
from netmiko import ConnectHandler


def create_conn(port: str) -> dict:
    return {
        "device_type": "juniper",
        "host": "localhost",
        "username": "root",
        "password": "Juniper",
        "port": port,
    }


if __name__ == "__main__":
    vsrx1 = create_conn("2201")
    vsrx1_conn = ConnectHandler(**vsrx1)
    vsrx1_conn.send_config_from_file("load_conf.conf")
    vsrx1_conn.commit()
    vsrx1_conn.disconnect()
