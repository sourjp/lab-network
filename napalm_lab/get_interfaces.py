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
        interfaces = conn.get_interfaces()
        for k, v in interfaces.items():
            if k.startswith("ge-"):
                print(k, v.get("mac_address"))
