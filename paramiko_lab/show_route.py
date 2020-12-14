#!/usr/bin/env python3
import paramiko
import time

device = {
    "host": "localhost",
    "port": "2201",
    "username": "root",
    "password": "Juniper",
}

if __name__ == "__main__":
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conn.connect(device["host"], port=device["port"],
                 username=device["username"], password=device["password"])
    router_conn = conn.invoke_shell()
    print(f'Successfully connected to {device["host"]}')

    router_conn.send("cli\n")
    router_conn.send("set cli screen-length 0\n")
    router_conn.send("show route\n")
    time.sleep(2)

    print(router_conn.recv(4092).decode("utf-8"))
