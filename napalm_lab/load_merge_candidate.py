from napalm import get_network_driver
import time

vsrx1_params = {
    "hostname": "localhost",
    "username": "root",
    "password": "Juniper",
    "optional_args": {"port": "2201"}
}

if __name__ == "__main__":
    junos_driver = get_network_driver("junos")

    CMD = [
        "set protocols bgp group ebgp type external",
        "set protocols bgp group ebgp export export-route",
        "set protocols bgp group ebgp peer-as 65002",
        "set protocols bgp group ebgp neighbor 192.168.1.2",
        "set policy-options policy-statement export-route term 1 from route-filter 10.0.0.1/32 exact",
        "set policy-options policy-statement export-route term 1 then accept"]

    with junos_driver(**vsrx1_params) as conn:
        target = "192.168.1.2"

        print(f"Test connectivity to {target}.")
        ping = conn.ping(target)
        if ping["success"]["packet_loss"] != 0:
            print(f"Couldn't reach to neigbor {target}.")
        print(f"Found {target}")

        print("Start installing config.")
        for cmd in CMD:
            conn.load_merge_candidate(config=cmd)

        diff = conn.compare_config()
        print("Diff:\n" + diff)

        while True:
            choice = input("Would you like to commit these changes? [y/N}: ")
            if choice in ["y", "yes", "Y"]:
                conn.commit_config()
                print("Config has commited.")
                break
            elif choice in ["n", "No", "N"]:
                conn.discard_config()
                print("Abort.")
                break

        print("Check BGP neighbor.")
        count = 0
        while count < 6:
            time.sleep(2)
            try:
                bgp = conn.get_bgp_neighbors()
                info = bgp["global"]["peers"].get(target)
                if info["is_enabled"]:
                    print(f"BGP neighbor {target} has up.")
                    break
            except BaseException:
                raise ValueError(f"Couldn't find {target} in BGP neighbors.")
            count += 1

        if count >= 5:
            print("Couldn't confirm BGP neighbor up. Check it directly.")
        print("Done")
