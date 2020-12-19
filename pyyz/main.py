#!/usr/bin/env python3
from jnpr.junos import Device
import json
from pprint import pprint
from lxml import etree

vsrx1_params = {
    "host": "localhost",
    "user": "root",
    "password": "Juniper",
    "port": "2201"
}

if __name__ == "__main__":
    with Device(**vsrx1_params) as conn:
        facts = conn.facts
        print(type(facts))
        pprint(facts)
