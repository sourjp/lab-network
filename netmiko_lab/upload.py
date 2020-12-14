#!/usr/bin/env python3
from netmiko import ConnectHandler, FileTransfer


def create_conn(port: str) -> dict:
    return {
        "device_type": "juniper_junos_ssh",
        "host": "localhost",
        "username": "root",
        "password": "Juniper",
        "port": port,
    }


if __name__ == "__main__":
    vsrx1 = create_conn("2201")
    vsrx1_conn = ConnectHandler(**vsrx1)

    with FileTransfer(vsrx1_conn,
                      source_file="load_conf.conf",
                      dest_file="load_conf.conf") as scp_transfer:
        if not scp_transfer.check_file_exists():
            if not scp_transfer.verify_space_available():
                raise ValueError("Insufficient space available on remote device")

            scp_transfer.transfer_file()
