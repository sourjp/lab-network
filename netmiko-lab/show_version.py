#!/usr/bin/env python3
from netmiko import ConnectHandler

SHOW_VERSION = "show version"


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
    vsrx2 = create_conn("2202")
    vsrx1_conn = ConnectHandler(**vsrx1, conn_timeout=30)
    vsrx2_conn = ConnectHandler(**vsrx2, conn_timeout=30)
    print(vsrx1_conn.send_command(SHOW_VERSION))
    print(vsrx2_conn.send_command(SHOW_VERSION))
    vsrx1_conn.disconnect()
    vsrx2_conn.disconnect()
