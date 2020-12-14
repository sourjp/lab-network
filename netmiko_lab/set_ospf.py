from netmiko import ConnectHandler

SHOW_OSPF = "show ospf neighbor"


def create_conn(port: str) -> dict:
    return {
        "device_type": "juniper",
        "host": "localhost",
        "username": "root",
        "password": "Juniper",
        "port": port,
    }


def create_ospf(n: str) -> list:
    return [
        f"set interfaces ge-0/0/1 unit 0 family inet address 192.168.0.{n}/30",
        f"set interfaces lo0 unit 0 family inet address 10.0.0.{n}/32",
        f"set routing-options router-id 10.0.0.{n}",
        "set protocols ospf area 0.0.0.0 interface lo0.0 passive",
        "set protocols ospf area 0.0.0.0 interface ge-0/0/1.0"
    ]


if __name__ == "__main__":
    vsrx1 = create_conn("2201")
    vsrx2 = create_conn("2202")
    vsrx1_conn = ConnectHandler(**vsrx1)
    vsrx2_conn = ConnectHandler(**vsrx2)
    vsrx1_conn.send_config_set(create_ospf("1"))
    vsrx2_conn.send_config_set(create_ospf("2"))
    vsrx1_conn.commit()
    vsrx2_conn.commit()
    vsrx1_conn.disconnect()
    vsrx2_conn.disconnect()

    vsrx1 = create_conn("2201")
    vsrx2 = create_conn("2202")
    vsrx1_conn = ConnectHandler(**vsrx1)
    vsrx2_conn = ConnectHandler(**vsrx2)
    print(vsrx1_conn.send_command(SHOW_OSPF))
    print(vsrx2_conn.send_command(SHOW_OSPF))
    vsrx1_conn.disconnect()
    vsrx2_conn.disconnect()
