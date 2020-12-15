from napalm import get_network_driver
import pprint

vsrx1_params = {
    "hostname": "localhost",
    "username": "root",
    "password": "Juniper",
    "optional_args": {"port": "2201"}
}

if __name__ == "__main__":
    junos_driver = get_network_driver("junos")

    with junos_driver(**vsrx1_params) as conn:
        arps = conn.get_arp_table()
        for arp in arps:
            print(type(arp))
            pprint.pprint(arp, indent=2)
