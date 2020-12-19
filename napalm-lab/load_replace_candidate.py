#!/usr/bin/env python3
from napalm import get_network_driver

vsrx1_params = {
    "hostname": "localhost",
    "username": "root",
    "password": "Juniper",
    "optional_args": {"port": "2201"}
}

if __name__ == "__main__":
    junos_driver = get_network_driver("junos")

    with junos_driver(**vsrx1_params) as conn:

        conn.load_replace_candidate(filename="config.conf")
        diff = conn.compare_config()
        print("Diff:\n" + diff)
